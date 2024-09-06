from django.forms import ModelForm #Textarea, TextInput, DateInput, DateField
from .models import Type_active, Name_active, Inventory_number, Owner_active, Status_active



class Type_active_Form(ModelForm):
    class Meta:
        model = Type_active
        fields = ('type_active',)
        # widgets = {
        #     "type_tmts": TextInput(attrs={"size":60,}),
        # }


class Name_active_Form(ModelForm):
    class Meta:
        model = Name_active
        fields = ('type_active', 'manufacturer', 'name_model',)



class Inventory_number_Form(ModelForm):
    class Meta:
        model = Inventory_number
        fields = ('inventory_number',)


class Owner_active_Form(ModelForm):
    class Meta:
        model = Owner_active
        fields = ('owner_active',)


class Status_active_Form(ModelForm):
    class Meta:
        model = Status_active
        fields = ('status',)


