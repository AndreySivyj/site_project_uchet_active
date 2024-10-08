from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'uchet_active'

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.name_active_list_view, name='name_active_list_view'),

    # ###########################################################################################################################################################
    # Справочники
    # ###########################################################################################################################################################
    
    # Model Type_active / Тип актива
    path('type_active_list_view/', views.type_active_list_view, name='type_active_list_view'),
    path('type_active/<int:id>/', views.type_active_detail_view, name='type_active_detail_view'),
    path('type_active_create/', views.type_active_create, name='type_active_create'),
    path('type_active_delete/<int:id>/', views.type_active_delete, name='type_active_delete'),
    path('type_active_update/<int:id>/', views.type_active_update, name='type_active_update'),

    # Model Name_active / Модели активов
    path('name_active_list_view/', views.name_active_list_view, name='name_active_list_view'),
    path('name_active/<int:id>/', views.name_active_detail_view, name='name_active_detail_view'),
    path('name_active_create/', views.name_active_create, name='name_active_create'),
    path('name_active_delete/<int:id>/', views.name_active_delete, name='name_active_delete'),
    path('name_active_update/<int:id>/', views.name_active_update, name='name_active_update'),

    # Model Inventory_number / Инвентарные номера
    path('inventory_number_list_view/', views.inventory_number_list_view, name='inventory_number_list_view'),
    path('inventory_number/<int:id>/', views.inventory_number_detail_view, name='inventory_number_detail_view'),
    path('inventory_number_create/', views.inventory_number_create, name='inventory_number_create'),
    path('inventory_number_delete/<int:id>/', views.inventory_number_delete, name='inventory_number_delete'),
    path('inventory_number_update/<int:id>/', views.inventory_number_update, name='inventory_number_update'),

    # Model Owner_active / Владелецы активов
    path('owner_active_list_view/', views.owner_active_list_view, name='owner_active_list_view'),
    path('owner_active/<int:id>/', views.owner_active_detail_view, name='owner_active_detail_view'),
    path('owner_active_create/', views.owner_active_create, name='owner_active_create'),
    path('owner_active_delete/<int:id>/', views.owner_active_delete, name='owner_active_delete'),
    path('owner_active_update/<int:id>/', views.owner_active_update, name='owner_active_update'),

    # Model Location_active / Локация/Склад
    path('location_active_list_view/', views.location_active_list_view, name='location_active_list_view'),
    path('location_active/<int:id>/', views.location_active_detail_view, name='location_active_detail_view'),
    path('location_active_create/', views.location_active_create, name='location_active_create'),
    path('location_active_delete/<int:id>/', views.location_active_delete, name='location_active_delete'),
    path('location_active_update/<int:id>/', views.location_active_update, name='location_active_update'),

    # Model Status_active / Статусы
    path('status_active_list_view/', views.status_active_list_view, name='status_active_list_view'),
    path('status_active/<int:id>/', views.status_active_detail_view, name='status_active_detail_view'),
    path('status_active_create/', views.status_active_create, name='status_active_create'),
    path('status_active_delete/<int:id>/', views.status_active_delete, name='status_active_delete'),
    path('status_active_update/<int:id>/', views.status_active_update, name='status_active_update'),

    # Model Name_quantity_active / Единицы измерения
    path('name_quantity_active_list_view/', views.name_quantity_active_list_view, name='name_quantity_active_list_view'),
    path('name_quantity_active/<int:id>/', views.name_quantity_active_detail_view, name='name_quantity_active_detail_view'),
    path('name_quantity_active_create/', views.name_quantity_active_create, name='name_quantity_active_create'),
    path('name_quantity_active_delete/<int:id>/', views.name_quantity_active_delete, name='name_quantity_active_delete'),
    path('name_quantity_active_update/<int:id>/', views.name_quantity_active_update, name='name_quantity_active_update'),

    # ###########################################################################################################################################################
    # Реестры
    # ###########################################################################################################################################################

    # Model Details_document_active / Реквизиты документов
    path('details_document_active_list_view/', views.details_document_active_list_view, name='details_document_active_list_view'),
    path('details_document_active/<int:id>/', views.details_document_active_detail_view, name='details_document_active_detail_view'),
    path('details_document_active_create/', views.details_document_active_create, name='details_document_active_create'),
    path('details_document_active_delete/<int:id>/', views.details_document_active_delete, name='details_document_active_delete'),
    path('details_document_active_update/<int:id>/', views.details_document_active_update, name='details_document_active_update'),

    # Model Profile_AD / Профили пользователей (AD)
    path('profile_ad_list_view/', views.profile_ad_list_view, name='profile_ad_list_view'),
    path('profile_ad/<int:id>/', views.profile_ad_detail_view, name='profile_ad_detail_view'),
    path('profile_ad_create/', views.profile_ad_create, name='profile_ad_create'),
    path('profile_ad_delete/<int:id>/', views.profile_ad_delete, name='profile_ad_delete'),
    path('profile_ad_update/<int:id>/', views.profile_ad_update, name='profile_ad_update'),

    # Model Receipt_active / Поступление активов
    path('receipt_active_list_view/', views.receipt_active_list_view, name='receipt_active_list_view'),
    path('receipt_active/<int:id>/', views.receipt_active_detail_view, name='receipt_active_detail_view'),
    path('receipt_active_create/', views.receipt_active_create, name='receipt_active_create'),
    path('receipt_active_delete/<int:id>/', views.receipt_active_delete, name='receipt_active_delete'),
    path('receipt_active_update/<int:id>/', views.receipt_active_update, name='receipt_active_update'),

    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)