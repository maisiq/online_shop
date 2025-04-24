from collections.abc import Mapping, Sequence

from django import forms

from online_shop.products.models import Product


class SelectItemsForm(forms.Form):
    '''Form which depends on items in user's cart. 

    ``items_id`` sequence of products ids in cart
    '''

    items = forms.ModelMultipleChoiceField(
        Product.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        error_messages={'required': 'Выберите хотя бы один товар'}
    )

    def __init__(self, *, items_id: Sequence[str], data: Mapping | None = None, **kwargs):
        super().__init__(data,  **kwargs)

        qs = Product.objects.filter(id__in=items_id).all()
        self.fields['items'].queryset = qs
