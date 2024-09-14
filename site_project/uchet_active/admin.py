from django.contrib import admin
from .admin_mixins import ExportAsCSVMixin
from .models import *


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
    list_filter = ['owner_active', 'location',]
    search_fields = ('owner_active', 'location',)
    ordering = ('owner_active', 'location',)


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
