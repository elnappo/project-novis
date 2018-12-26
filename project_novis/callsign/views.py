from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Country, DXCCEntry, CallSign, DMRID, CallSignPrefix
from .serializers import CountrySerializer, DXCCEntrySerializer, CallsignSerializer,\
    DMRIDSerializer, CallSignPrefixSerializer


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
    fields = ["type", 'cq_zone', "itu_zone", "grid", "latitude", "longitude", "issued", "active", "dstar"]
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

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    permission_classes = (IsAuthenticatedOrReadOnly,)


class DMRIDFilter(rest_framework.FilterSet):
    class Meta:
        model = DMRID
        fields = {
            'active': ['exact'],
            'callsign__name': ['exact'],
            'issued': ['year', 'month', 'week', 'range', 'lt', 'gt'],
        }


class DMRIDViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DMRID.objects.all()
    serializer_class = DMRIDSerializer
    lookup_field = "name"
    pagination_class = DefaultPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = DMRIDFilter
    search_fields = ('name',)

    permission_classes = (IsAuthenticatedOrReadOnly,)


class DXCCEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DXCCEntry.objects.all()
    serializer_class = DXCCEntrySerializer
    pagination_class = DefaultPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('deleted',)
    search_fields = ('name',)

    permission_classes = (IsAuthenticatedOrReadOnly,)


class CallSignPrefixViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CallSignPrefix.objects.all()
    serializer_class = CallSignPrefixSerializer
    lookup_field = "name"
    pagination_class = DefaultPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('country', 'cq_zone', 'itu_zone', 'itu_region', 'continent', 'type')
    search_fields = ('name',)

    permission_classes = (IsAuthenticatedOrReadOnly,)


class CallSignViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CallSign.objects.all()
    serializer_class = CallsignSerializer
    lookup_field = 'name'
    pagination_class = DefaultPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('active', 'issued')
    search_fields = ('name',)

    permission_classes = (IsAuthenticatedOrReadOnly,)


class CallSignCreateAPIView(generics.CreateAPIView):
    queryset = CallSign.objects.all()
    serializer_class = CallsignSerializer

    permission_classes = (IsAuthenticated,)


class UserCallSignViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'name'
    queryset = CallSign.objects.all()
    serializer_class = CallsignSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.callsign_set.all()
