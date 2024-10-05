import django_filters
from .models import *
from django.forms.widgets import DateInput


# ###########################################################################################################################################################
# Справочники
# ###########################################################################################################################################################

class Type_active_Filter(django_filters.FilterSet):
    # id = django_filters.NumberFilter(field_name="id", lookup_expr='in')
    type_active = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Type_active
        # fields = ['id', 'type_active', ]
        fields = ['type_active', ]


class Name_active_Filter(django_filters.FilterSet):
    manufacturer = django_filters.CharFilter(lookup_expr='icontains')
    name_model = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Name_active
        fields = ['type_active', 'manufacturer', 'name_model']


class Inventory_number_Filter(django_filters.FilterSet):    
    inventory_number = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Inventory_number
        fields = ['inventory_number', ]


class Owner_active_Filter(django_filters.FilterSet):    
    owner_active = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Owner_active
        fields = ['owner_active', ]


class Location_active_Filter(django_filters.FilterSet):
    location = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Location_active
        fields = ['owner_active', 'location']


class Status_active_Filter(django_filters.FilterSet):    
    status = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Status_active
        fields = ['status', ]


class Name_quantity_active_Filter(django_filters.FilterSet):
    name_quantity = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Name_quantity_active
        fields = ['name_quantity']


# ###########################################################################################################################################################
# Реестры
# ###########################################################################################################################################################

class Details_document_active_Filter(django_filters.FilterSet):
    name_document = django_filters.CharFilter(lookup_expr='icontains')
    shipping_location = django_filters.CharFilter(lookup_expr='icontains')
    comment = django_filters.CharFilter(lookup_expr='icontains')
    created = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), lookup_expr='icontains')
    # creator_account = django_filters.CharFilter(lookup_expr='icontains')
    updated = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), lookup_expr='icontains')
    
    class Meta:
        model = Details_document_active
        fields = ['name_document', 'shipping_location', 'comment', 'created', 'creator_account', 'updated',]


class Profile_AD_Filter(django_filters.FilterSet):
    account = django_filters.CharFilter(lookup_expr='icontains')
    fio = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    distingished_name = django_filters.CharFilter(lookup_expr='icontains')
    company = django_filters.CharFilter(lookup_expr='icontains')
    company_position = django_filters.CharFilter(lookup_expr='icontains')
    mobile = django_filters.CharFilter(lookup_expr='icontains')
    telephone_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Profile_AD
        fields = ['account', 'fio', 'email', 'distingished_name', 'company', 'company_position', 'mobile', 'telephone_number',]


class Receipt_active_Filter(django_filters.FilterSet):
    quantity = django_filters.NumberFilter(lookup_expr='icontains')
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    comment = django_filters.CharFilter(lookup_expr='icontains')
    created = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), lookup_expr='icontains')
    updated = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), lookup_expr='icontains')

    class Meta:
        model = Receipt_active
        fields = ['details_document_active', 'inventory_number', 'name_active', 'location_active', 
                    'name_quantity_active', 'quantity', 'serial_number', 'comment', 'created', 'creator_account', 'updated',]


