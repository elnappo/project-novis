from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Country, DXCCEntry, CallSign
from .serializers import CountrySerializer, DXCCEntrySerializer, CallsignSerializer


class DefaultPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 100


class CallSignDetailView(DetailView):
    model = CallSign
    slug_field = "name"


@method_decorator(login_required(), name='dispatch')
class CallSignCreate(CreateView):
    model = CallSign
    fields = ['name']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.set_default_meta_data()
        return super().form_valid(form)


@method_decorator(login_required(), name='dispatch')
class CallSignUpdate(UpdateView):
    model = CallSign
    slug_field = "name"
    fields = ["type", 'cq_zone', "itu_zone", "grid", "latitude", "longitude", "issued", "active"]
    template_name_suffix = '_update_form'


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class DXCCEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DXCCEntry.objects.all()
    serializer_class = DXCCEntrySerializer
    pagination_class = DefaultPagination


class CallSignViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CallSign.objects.all()
    serializer_class = CallsignSerializer
    pagination_class = DefaultPagination
