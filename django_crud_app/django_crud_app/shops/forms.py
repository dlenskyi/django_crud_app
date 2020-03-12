from django import forms
from .models import Shop


class ShopForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['shop_number'].required = True
        self.fields['owner'].required = True

    class Meta:
        model = Shop
        fields = ['name', 'shop_number', 'owner', ]
