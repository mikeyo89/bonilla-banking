from django.db import models
from django.conf import settings
from address.models import AddressField

# Create your models here.
class BankAccountsModel(models.Model):
    """
    Model of bank accounts -- checkings, savings, credit.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=1000)
    name = models.CharField(max_length=30)

    ACCOUNT_TYPE_CHOICES = [
        ('checkings', 'Checkings'),
        ('savings', 'Savings'),
        ('credit', 'Credit')
    ]
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    account_number = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')

    def __str__(self):
        return f'{ str(self.name) } - { str(self.account_number)[-4:] }'

class TransactionsModel(models.Model):
    """
    Model of bank account transactions -- Debit, Credit, transfers, payments, deposits.
    """
    account = models.ForeignKey('BankAccountsModel', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date of Transaction')
    new_balance = models.DecimalField(max_digits=7, decimal_places=2)

    TRANSACTION_TYPE_CHOICES = [
        ('payment', 'Payment'),     # A debit towards a bill payment.
        ('debit', 'Debit'),         # A cost/expense incured.
        ('credit', 'Credit'),       # A return of money, a deposit, or a gain.
        ('transfer', 'Transfer')    # Exchanging money between personal accounts.
    ]

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField()
    label = models.CharField(max_length=128)
    scheduled_date = models.DateField(null=True, blank=True)

class PaymentConnectionsModel(models.Model):
    """
    Model that establishes bill pay registration between user and bill corporations.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    corporation = models.ForeignKey('CorporationsModel', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')

    def __str__(self):
        return f'{self.corporation}'

class CorporationsModel(models.Model):
    """
    Model that lists the corporations that have partnered with Bonilla Banking.
    """
    name = models.CharField(max_length=128)
    bill_type = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')

    def __str__(self):
        return f'{self.name}'