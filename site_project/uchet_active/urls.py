from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'uchet_active'

urlpatterns = [
    path('', views.index, name='index'),
    # path('', views.name_active_list_view, name='name_active_list_view'),
    
    # Model Type_active / Тип актива
    path('type_active_list_view/', views.type_active_list_view, name='type_active_list_view'),
    path('type_active/<int:id>/', views.type_active_detail_view, name='type_active_detail_view'),

    # Model Name_active / Модели активов
    path('name_active_list_view/', views.name_active_list_view, name='name_active_list_view'),
    path('name_active/<int:id>/', views.name_active_detail_view, name='name_active_detail_view'),

    # Model Inventory_number / Инвентарные номера
    path('inventory_number_list_view/', views.inventory_number_list_view, name='inventory_number_list_view'),
    path('inventory_number/<int:id>/', views.inventory_number_detail_view, name='inventory_number_detail_view'),

    # Model Owner_active / Владелецы активов
    path('owner_active_list_view/', views.owner_active_list_view, name='owner_active_list_view'),
    path('owner_active/<int:id>/', views.owner_active_detail_view, name='owner_active_detail_view'),

    # Model Status_active / Статусы
    path('status_active_list_view/', views.status_active_list_view, name='status_active_list_view'),
    path('status_active/<int:id>/', views.status_active_detail_view, name='status_active_detail_view'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)