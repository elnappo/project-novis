from django.contrib.gis import forms
from dal import autocomplete

from .models import CallSign


class CallsignForm(forms.ModelForm):
    issued = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),
                             required=False)
    location = forms.PointField(srid=4326,
                                widget=forms.OSMWidget(attrs={'map_width': 785, 'map_height': 500, 'default_zoom': 12}))

    class Meta:
        model = CallSign
        fields = ["type", "location", 'cq_zone', "itu_zone", "dstar", "issued"]
