# Generated by Django 4.2.14 on 2024-10-05 06:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uchet_active', '0008_alter_profile_ad_account_receipt_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt_active',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]
