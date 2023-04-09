from django import forms
from django.core.validators import MinValueValidator
from .models import Inbound, Outbound


class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if data <= 0:
            raise forms.ValidationError("재고가 부족합니다.")
        return data


class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if data <= 0:
            raise forms.ValidationError("재고가 부족합니다.")
        return data
