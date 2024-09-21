import django_filters
from .models import *


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

