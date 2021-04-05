# Generated by Django 3.1.7 on 2021-04-03 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountmodel',
            name='date_of_birth',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='accountmodel',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='accountmodel',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='accountmodel',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
