from django import forms

from .models import Discount


class AddDiscountForm(forms.Form):
    discount = forms.CharField(max_length=64, required=True)

    def clean_discount(self):
        code = self.cleaned_data['discount']
        discount = Discount.objects.filter(name=code.upper()).first()
    
        if not discount or discount.type == Discount.DiscountType.PRODUCT_WIDE:
            raise forms.ValidationError('Недействительный промокод', 'invalid')
        if not discount.is_active:
            raise forms.ValidationError('Срок действия промокода истек', 'invalid')

        return code