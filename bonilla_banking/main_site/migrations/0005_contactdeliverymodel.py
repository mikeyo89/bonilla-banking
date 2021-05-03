# Generated by Django 3.1.7 on 2021-05-01 19:39

import address.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_auto_20200830_1851'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_site', '0004_corporationsmodel_paymentconnectionsmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDeliveryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, to='address.address')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
