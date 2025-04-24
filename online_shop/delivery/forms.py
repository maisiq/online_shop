from django import forms

from .models import Delivery


class OptDeliveryForm(forms.Form):
    '''
        Form for choosing delivery during order process.
        If no user passed when init then returns no Delivery objects.

    '''
    delivery = forms.ModelChoiceField(
        Delivery.objects.none(),
        widget=forms.Select,
        empty_label=None,
    )

    def __init__(self, *, user=None, **kwargs):
        super().__init__(**kwargs)
        if user:
            self.fields['delivery'].queryset = Delivery.objects.filter(customer=user)


class CreateDeliveryForm(forms.ModelForm):
    receiver = forms.CharField(widget=forms.TextInput)
    address = forms.CharField(widget=forms.TextInput)
    type = forms.ChoiceField(choices=Delivery.DeliveryTypes.choices)

    class Meta:
        model = Delivery
        fields = ['type', 'receiver', 'receiver_phone', 'address']
