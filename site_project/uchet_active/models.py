from django.db import models
from django.urls import reverse
from django.conf import settings


# ###########################################################################################################################################################
# Справочники
# ###########################################################################################################################################################

class Type_active(models.Model):
    type_active = models.CharField(max_length=50, verbose_name='Тип актива', unique=True, db_index=True)    
    
    class Meta:
        # db_table='Type_active' # указание имени таблицы в базе данных "вручную"
        verbose_name_plural = '(1.1) Типы активов'
        verbose_name = 'Тип актива'
        ordering = ['type_active',]
    
    def __str__(self):
        return f"{self.type_active}"
    
    def get_absolute_url(self):
        return reverse('uchet_active:type_active_detail_view', args=[self.id,])


class Name_active(models.Model):
    type_active = models.ForeignKey('Type_active', on_delete=models.PROTECT, verbose_name='Тип актива')
    manufacturer = models.CharField(max_length=50, verbose_name='Производитель', db_index=True)
    name_model = models.CharField(max_length=50, verbose_name='Модель', db_index=True)
    
    class Meta:
        verbose_name_plural = '(1.2) Модели активов'
        verbose_name = 'Модель актива'
        ordering = ['type_active', 'manufacturer', 'name_model']
    
    def __str__(self):        
        return f"{self.type_active.type_active} {self.manufacturer} {self.name_model}"
    
    def get_absolute_url(self):
        return reverse('uchet_active:name_active_detail_view', args=[self.id,])


class Inventory_number(models.Model):
    inventory_number = models.CharField(max_length=50, verbose_name='Инвентарный номер', unique=True, db_index=True)
    
    class Meta:
        verbose_name_plural = '(1.3) Инвентарные номера'
        verbose_name = 'Инвентарный номер'
        ordering = ['inventory_number',]

    def __str__(self):
        return f"{self.inventory_number}"
    
    def get_absolute_url(self):
        return reverse('uchet_active:inventory_number_detail_view', args=[self.id,])


class Name_quantity_active(models.Model):
    name_quantity = models.CharField(max_length=25, verbose_name='Ед.изм-я', unique=True, db_index=True)   
    
    class Meta:        
        verbose_name_plural = '(1.4) Единицы измерения'
        verbose_name = 'Единица измерения'
        ordering = ['name_quantity',]
    
    def __str__(self):
        return f"{self.name_quantity}"
    
    def get_absolute_url(self):
        return reverse('uchet_active:name_quantity_active_detail_view', args=[self.id,])


class Status_active(models.Model):
    status = models.CharField(max_length=25, verbose_name='Статус', unique=True, db_index=True)   
    
    class Meta:        
        verbose_name_plural = '(1.5) Статусы'
        verbose_name = 'Статус'
        ordering = ['status',]
    
    def __str__(self):
        return f"{self.status}"
    
    def get_absolute_url(self):
        return reverse('uchet_active:status_active_detail_view', args=[self.id,])


class Owner_active(models.Model):
    owner_active = models.CharField(max_length=150, verbose_name='Владелец актива', unique=True, db_index=True)
    
    class Meta:
        verbose_name_plural = '(1.6) Владелецы активов'
        verbose_name = 'Владелец актива'
        ordering = ['owner_active',]
    
    def __str__(self):
        return f"{self.owner_active}"
    
    def get_absolute_url(self):
        return reverse('uchet_active:owner_active_detail_view', args=[self.id,])


class Location_active(models.Model):
    owner_active = models.ForeignKey('Owner_active', on_delete=models.PROTECT, verbose_name='Владелец актива')
    location = models.CharField(max_length=150, verbose_name='Локация/Склад', db_index=True)           
    
    class Meta:        
        verbose_name_plural = '(1.7) Локация/Склад'
        verbose_name = 'Локация/Склад'
        ordering = ['owner_active','location',]
    
    def __str__(self):
        return f"{self.owner_active}, {self.location}"
    
    def get_absolute_url(self):
        return reverse('uchet_active:location_active_detail_view', args=[self.id,])



# ###########################################################################################################################################################
# Реестры
# ###########################################################################################################################################################

class Details_document_active(models.Model):
    name_document = models.CharField(max_length=50, verbose_name='Документ', db_index=True)
    shipping_location = models.CharField(max_length=150, verbose_name='Локация/Склад отгрузки', db_index=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи', db_index=True)    
    creator_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Кем изменено/создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения записи')    
    
    class Meta:        
        verbose_name_plural = '(2.1) Реквизиты документов'
        verbose_name = 'Реквизиты документа'
        ordering = ['name_document','shipping_location',]
    
    def __str__(self):
        return f"{self.name_document}"
    
    def get_absolute_url(self):
        return reverse('uchet_active:details_document_active_detail_view', args=[self.id,])


class Profile_AD(models.Model):
    account = models.CharField(max_length=50, verbose_name='Учетная запись')
    fio = models.CharField(max_length=75, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Email')
    distingished_name = models.CharField(max_length=175, verbose_name='Имя объекта')
    company = models.CharField(max_length=75, blank=True, verbose_name='Юридическое лицо')
    company_position = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    mobile = models.CharField(max_length=35, blank=True, verbose_name='Телефон (мобильный)')
    telephone_number = models.CharField(max_length=35, blank=True, verbose_name='Телефон')

    class Meta:        
        verbose_name_plural = '(2.2) Профили пользователей (AD)'
        verbose_name = 'Профиль пользователя (AD)'
        ordering = ['account',]
    
    def __str__(self):
        return f"{self.account}"
    
    def get_absolute_url(self):
        return reverse('uchet_active:profile_ad_detail_view', args=[self.id,])



