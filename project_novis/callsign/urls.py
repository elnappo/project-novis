from django.urls import path

from .views import CallsignDetailView, CallsignCreate, CallsignUpdate, CallsignClaimView, RepeaterUpdate, ClubUpdate,\
    CallsignAutocomplete

app_name = "callsign"

urlpatterns = [
    path('add/', CallsignCreate.as_view(), name='callsign-html-create'),
    path('autocomplete/', CallsignAutocomplete.as_view(), name='callsign-autocomplete'),

    path('<slug>/', CallsignDetailView.as_view(), name='callsign-html-detail'),
    path('<slug>/change', CallsignUpdate.as_view(), name='callsign-html-update'),
    path('<slug>/repeater/change', RepeaterUpdate.as_view(), name='repeater-html-update'),
    path('<slug>/club/change', ClubUpdate.as_view(), name='club-html-update'),
    path('<slug>/claim', CallsignClaimView.as_view(), name='callsign-html-claim'),
]
