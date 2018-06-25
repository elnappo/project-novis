from django.views.generic.detail import DetailView

from .models import Callsign


class CallsignDetailView(DetailView):
    model = Callsign
    slug_field = "name"
