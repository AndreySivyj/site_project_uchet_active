# Generated by Django 4.2.14 on 2024-10-05 00:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uchet_active', '0007_profile_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_ad',
            name='account',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Учетная запись'),
        ),
        migrations.CreateModel(
            name='Receipt_active',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
                ('serial_number', models.CharField(blank=True, max_length=50, verbose_name='S/N')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания записи')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')),
                ('creator_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Кем изменено/создано')),
                ('details_document_active', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='uchet_active.details_document_active', verbose_name='Реквизиты документа')),
                ('inventory_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='uchet_active.inventory_number', verbose_name='Инвентарный номер')),
                ('location_active', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='uchet_active.location_active', verbose_name='Локация/Склад')),
                ('name_active', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='uchet_active.name_active', verbose_name='Модель актива')),
                ('name_quantity_active', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='uchet_active.name_quantity_active', verbose_name='Ед.изм-я')),
            ],
            options={
                'verbose_name': 'Поступление актива',
                'verbose_name_plural': '(2.3) Поступление активов',
                'ordering': ['created'],
            },
        ),
    ]
