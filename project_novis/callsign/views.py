from csp.decorators import csp_update
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
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
from rest_framework_gis.filters import DistanceToPointFilter

from .forms import CallsignForm, RepeaterForm, ClubForm
from .models import Country, DXCCEntry, Callsign, DMRID, CallsignPrefix, Repeater, Club
from .serializers import CountrySerializer, DXCCEntrySerializer, CallsignSerializer, \
    DMRIDSerializer, CallsignPrefixSerializer, RepeaterSerializer, APRSPasscodeSerializer


class CallsignAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Callsign.objects.none()

        qs = Callsign.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class DefaultPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 100


@method_decorator(csp_update(IMG_SRC=(
    "maps.googleapis.com",  # Google Maps
    "maps.gstatic.com",  # Google Maps
    "cbks0.googleapis.com",
    "khms0.googleapis.com",
    "khms1.googleapis.com",
    "lh3.ggpht.com",
    "geo0.ggpht.com",  # Google Street View
    "geo1.ggpht.com",  # Google Street View
    "geo2.ggpht.com",  # Google Street View
    "geo3.ggpht.com",  # Google Street View
    ), SCRIPT_SRC=("maps.googleapis.com", "maps.gstatic.com")), name='dispatch')
class CallsignDetailView(DetailView):
    queryset = Callsign.objects\
        .select_related("prefix") \
        .select_related("prefix__dxcc") \
        .select_related("owner")\
        .select_related("country") \
        .select_related("country__telecommunicationagency") \
        .select_related("clubloguser") \
        .select_related("repeater")\
        .select_related("club") \
        .prefetch_related("dmr_ids")
    slug_field = "name"


class CallsignCreate(LoginRequiredMixin, CreateView):
    model = Callsign
    fields = ['name']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.source = "user"
        obj.set_default_meta_data()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        existing_callsign = Callsign.objects.filter(name=form.data.get('name')).first()
        if existing_callsign:
            return redirect(existing_callsign)
        return super().post(request, *args, **kwargs)


@method_decorator(csp_update(IMG_SRC=("*.tile.openstreetmap.org",)), name='dispatch')
class CallsignUpdate(LoginRequiredMixin, UpdateView):
    model = Callsign
    slug_field = "name"
    form_class = CallsignForm
    template_name_suffix = '_update_form'

    # TODO(elnappo) Replace permission check with django-guardian?
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner == request.user or not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class RepeaterUpdate(LoginRequiredMixin, UpdateView):
    model = Repeater
    slug_field = "callsign__name"
    form_class = RepeaterForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('callsign:callsign-html-detail', args=[self.object.callsign.name])

    # TODO(elnappo) Replace permission check with django-guardian?
    def dispatch(self, request, *args, **kwargs):
        # Create an Repeater instance if does not exist
        try:
            self.get_object()
        except Http404:
            slug = self.kwargs.get(self.slug_url_kwarg)
            try:
                callsign_instance = Callsign.objects.get(name=slug)
                if request.user.is_authenticated and callsign_instance.owner != request.user:
                    return HttpResponseForbidden()
                elif not request.user.is_authenticated:
                    return super().dispatch(request, *args, **kwargs)
                self.model.objects.create(callsign=callsign_instance, created_by_id=request.user.id)
            except Callsign.DoesNotExist:
                raise Http404(_("No callsign found matching the query") %
                              {'verbose_name': Callsign._meta.verbose_name})

        if self.get_object().callsign.owner == request.user or not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


@method_decorator(csp_update(CONNECT_SRC=("'self'",)), name='dispatch')
class ClubUpdate(LoginRequiredMixin, UpdateView):
    model = Club
    slug_field = "callsign__name"
    form_class = ClubForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('callsign:callsign-html-detail', args=[self.object.callsign.name])

    # TODO(elnappo) Replace permission check with django-guardian?
    def dispatch(self, request, *args, **kwargs):
        # Create an Club instance if does not exist
        try:
            self.get_object()
        except Http404:
            slug = self.kwargs.get(self.slug_url_kwarg)
            try:
                callsign_instance = Callsign.objects.get(name=slug)
                if request.user.is_authenticated and callsign_instance.owner != request.user:
                    return HttpResponseForbidden()
                elif not request.user.is_authenticated:
                    return super().dispatch(request, *args, **kwargs)
                self.model.objects.create(callsign=callsign_instance, created_by_id=request.user.id)
            except Callsign.DoesNotExist:
                raise Http404(_("No callsign found matching the query") %
                              {'verbose_name': Callsign._meta.verbose_name})

        if self.get_object().callsign.owner == request.user or not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class CallsignClaimView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Callsign
    slug_field = "name"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(self.object)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.user.claim_call_sign(self.object)
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


class CallsignPrefixViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CallsignPrefix.objects.all()
    serializer_class = CallsignPrefixSerializer
    lookup_field = "name"
    pagination_class = DefaultPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('country', 'cq_zone', 'itu_zone', 'itu_region', 'continent', 'type')
    search_fields = ('name',)

    permission_classes = (IsAuthenticatedOrReadOnly,)


class CallsignViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Callsign.objects.all()
    serializer_class = CallsignSerializer
    lookup_field = 'name'
    pagination_class = DefaultPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, DistanceToPointFilter)
    filterset_fields = ('active', 'issued')
    search_fields = ('name',)
    distance_filter_field = 'location'

    permission_classes = (IsAuthenticatedOrReadOnly,)


class RepeaterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repeater.objects.all()
    serializer_class = RepeaterSerializer
    lookup_field = 'callsign__name'
    pagination_class = DefaultPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, DistanceToPointFilter)
    filterset_fields = ('active',)
    search_fields = ('callsign__name',)
    distance_filter_field = 'location'

    permission_classes = (IsAuthenticatedOrReadOnly,)


class CallsignCreateAPIView(generics.CreateAPIView):
    queryset = Callsign.objects.all()
    serializer_class = CallsignSerializer

    permission_classes = (IsAuthenticated,)


class UserCallsignViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'name'
    queryset = Callsign.objects.all()
    serializer_class = CallsignSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.callsign_set.all()


class APRSPasscodeView(generics.RetrieveAPIView):
    lookup_field = 'name'
    queryset = Callsign.objects.all()
    serializer_class = APRSPasscodeSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.callsign_set.all()
