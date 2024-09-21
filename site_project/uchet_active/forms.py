from django.forms import ModelForm #Textarea, TextInput, DateInput, DateField
from .models import *
from django_select2 import forms as s2forms



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


