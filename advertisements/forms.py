from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AdvertisementURLForm(forms.Form):
    url = forms.URLField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(AdvertisementURLForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
