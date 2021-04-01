from django.db import models

# Create your models here.
class SupportModel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=64)
    message = models.TextField()
    date_received = models.DateField(auto_now_add=True)

    def full_name(self):
        return f'{first_name} {last_name}'