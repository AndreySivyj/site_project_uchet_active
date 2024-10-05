from django.forms import ModelForm #Textarea, TextInput, DateInput, DateField
from .models import *
from django_select2 import forms as s2forms


# ###########################################################################################################################################################
# Справочники
# ###########################################################################################################################################################

class Type_active_Form(ModelForm):
    class Meta:
        model = Type_active
        fields = ('type_active',)   # '__all__'
        # widgets = {
        #     "type_tmts": TextInput(attrs={"size":60,}),
        # }


# class TypeActiveWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "type_active__icontains",
#     ]

class Name_active_Form(ModelForm):
    class Meta:
        model = Name_active
        fields = ('type_active', 'manufacturer', 'name_model',)
        # widgets = {
        #     "type_active": TypeActiveWidget,            
        # }


class Inventory_number_Form(ModelForm):
    class Meta:
        model = Inventory_number
        fields = ('inventory_number',)


class Owner_active_Form(ModelForm):
    class Meta:
        model = Owner_active
        fields = ('owner_active',)


class Location_active_Form(ModelForm):
    class Meta:
        model = Location_active
        fields = ('owner_active','location',)


class Status_active_Form(ModelForm):
    class Meta:
        model = Status_active
        fields = ('status',)


class Name_quantity_active_Form(ModelForm):
    class Meta:
        model = Name_quantity_active
        fields = ('name_quantity',)


# ###########################################################################################################################################################
# Реестры
# ###########################################################################################################################################################

class Details_document_active_Form(ModelForm):
    class Meta:
        model = Details_document_active
        fields = ('name_document', 'shipping_location', 'comment',)


class Profile_AD_Form(ModelForm):
    class Meta:
        model = Profile_AD
        fields = ('account',) # 'fio', 'email', 'distingished_name', 'company', 'company_position', 'mobile', 'telephone_number',


class Receipt_active_Form(ModelForm):
    class Meta:
        model = Receipt_active
        fields = ('details_document_active', 'inventory_number', 'name_active', 'location_active', 
                    'name_quantity_active', 'quantity', 'serial_number', ) 


