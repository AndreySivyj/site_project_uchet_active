from django.contrib import admin
from .admin_mixins import ExportAsCSVMixin
from .models import *


# ###########################################################################################################################################################
# Справочники
# ###########################################################################################################################################################

@admin.register(Type_active)
class Type_active_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'type_active',)
    list_display_links = ('type_active',)
    list_filter = ['type_active',]
    search_fields = ('type_active',)
    ordering = ('type_active',)


@admin.register(Name_active)
class Name_active_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'type_active', 'manufacturer', 'name_model',)
    list_display_links = ('manufacturer', 'name_model',)
    list_filter = ['type_active__type_active', 'manufacturer', 'name_model',]
    search_fields = ('type_active__type_active', 'manufacturer', 'name_model',)
    ordering = ('type_active__type_active', 'manufacturer', 'name_model',)


@admin.register(Inventory_number)
class Inventory_number_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'inventory_number',)
    list_display_links = ('inventory_number',)
    list_filter = ['inventory_number',]
    search_fields = ('inventory_number',)
    ordering = ('inventory_number',)


@admin.register(Owner_active)
class Owner_active_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'owner_active',)
    list_display_links = ('owner_active',)
    list_filter = ['owner_active',]
    search_fields = ('owner_active',)
    ordering = ('owner_active',)


@admin.register(Location_active)
class Location_active_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'owner_active', 'location',)
    list_display_links = ('location',)
    list_filter = ['owner_active__owner_active', 'location',]
    search_fields = ('owner_active__owner_active', 'location',)
    ordering = ('owner_active__owner_active', 'location',)


@admin.register(Status_active)
class Status_active_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'status',)
    list_display_links = ('status',)
    list_filter = ['status',]
    search_fields = ('status',)
    ordering = ('status',)


@admin.register(Name_quantity_active)
class Name_quantity_active_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'name_quantity',)
    list_display_links = ('name_quantity',)
    list_filter = ['name_quantity',]
    search_fields = ('name_quantity',)
    ordering = ('name_quantity',)


# ###########################################################################################################################################################
# Реестры
# ###########################################################################################################################################################

@admin.register(Details_document_active)
class Details_document_active_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'name_document', 'shipping_location', 'comment', 'created', 'creator_account', 'updated',)
    list_display_links = ('name_document',)
    list_filter = ['name_document', 'shipping_location', 'comment', 'created', 'creator_account__username', 'updated',]
    search_fields = ('name_document', 'shipping_location', 'comment', 'created', 'creator_account__username', 'updated',)
    ordering = ('created', 'name_document',)


@admin.register(Profile_AD)
class Profile_AD_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'account', 'fio', 'email', 'distingished_name', 'company', 'company_position', 'mobile', 'telephone_number',)
    list_display_links = ('account', 'fio',)
    list_filter = ['account', 'fio', 'email', 'distingished_name', 'company', 'company_position', 'mobile', 'telephone_number',]
    search_fields = ('account', 'fio', 'email', 'distingished_name', 'company', 'company_position', 'mobile', 'telephone_number',)
    ordering = ('account', 'fio',)


@admin.register(Receipt_active)
class Receipt_active_Admin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [        
        'export_csv',
    ]

    list_display = ('id', 'details_document_active', 'inventory_number', 'name_active', 'location_active', 
                    'name_quantity_active', 'quantity', 'serial_number', 'comment', 'created', 'creator_account', 'updated',)
    list_display_links = ('details_document_active', 'inventory_number', 'name_active',)
    list_filter = ['details_document_active__name_document', 'inventory_number__inventory_number', 'name_active__name_model', 
                    'location_active__location', 'serial_number', 'created', 'creator_account__username', 'updated',]
    search_fields = ('details_document_active__name_document', 'inventory_number__inventory_number', 'name_active__name_model', 'location_active__location', 
                    'name_quantity_active__name_quantity', 'quantity', 'serial_number', 'comment', 'created', 'creator_account__username', 'updated',)
    ordering = ('created',)




