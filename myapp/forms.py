from django import forms

from .models import Product


class DatalistTextInput(forms.TextInput):
    template_name = 'widgets/datalist_textinput.html'

    def __init__(self, datalist=None, data_list_id='brand-list', *args, **kwargs):
        self.data_list = datalist or []
        self.data_list_id = data_list_id
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['list'] = self.data_list_id
        context['data_list'] = self.data_list
        context['list_id'] = self.data_list_id
        return context


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brands = (Product.objects.exclude(brand='')
                  .values_list('brand', flat=True)
                  .distinct()
                  .order_by('brand'))
        self.fields['brand'].widget = DatalistTextInput(
            datalist=brands,
            data_list_id='brand-options'
        )
        self.fields['brand'].widget.attrs.setdefault(
            'placeholder', 'Start typing or pick an existing brand'
        )

