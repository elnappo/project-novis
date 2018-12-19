from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _
from django.views import View
from rest_framework import viewsets, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .models import Country, DXCCEntry, CallSign
from .serializers import CountrySerializer, DXCCEntrySerializer, CallsignSerializer, MinimalCallsignSerializer


class DefaultPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 100


class CallSignDetailView(DetailView):
    model = CallSign
    slug_field = "name"


class CallSignCreate(LoginRequiredMixin, CreateView):
    model = CallSign
    fields = ['name']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.set_default_meta_data()
        return super().form_valid(form)


class CallSignUpdate(LoginRequiredMixin, UpdateView):
    model = CallSign
    slug_field = "name"
    fields = ["type", 'cq_zone', "itu_zone", "grid", "latitude", "longitude", "issued", "active"]
    template_name_suffix = '_update_form'

    #TODO(elnappo) Replace permission check with django-guardian?
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class CallSignClaimView(LoginRequiredMixin, SingleObjectMixin, View):
    model = CallSign
    slug_field = "name"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(self.object)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.user.claim_call_sign(self.object)
        return redirect(self.object)


class CallSignSearchView(SingleObjectMixin, View):
    model = CallSign
    slug_field = "name"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(self.object)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(self.object)


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "id"


class DXCCEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DXCCEntry.objects.all()
    serializer_class = DXCCEntrySerializer
    pagination_class = DefaultPagination


class CallSignViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'name'
    queryset = CallSign.objects.all()
    serializer_class = CallsignSerializer
    pagination_class = DefaultPagination


class CallSignCreateAPIView(generics.CreateAPIView):
    queryset = CallSign.objects.all()
    serializer_class = MinimalCallsignSerializer
    permission_classes = (IsAuthenticated,)


class UserCallSignViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'name'
    queryset = CallSign.objects.all()
    serializer_class = CallsignSerializer

    def get_queryset(self):
        user = self.request.user
        return user.callsign_set.all()
