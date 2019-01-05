from django import forms

from .models import CallSign


class CallsignForm(forms.ModelForm):
    issued = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),
                             required=False)

    class Meta:
        model = CallSign
        fields = ["type", 'cq_zone', "itu_zone", "grid", "dstar", "issued"]
