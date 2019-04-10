from django.urls import path

from .views import CallsignDetailView, CallsignCreate, CallsignUpdate, CallsignClaimView

app_name = "callsign"

urlpatterns = [
    path('add/', CallsignCreate.as_view(), name='callsign-html-create'),

    path('<slug>/', CallsignDetailView.as_view(), name='callsign-html-detail'),
    path('<slug>/change', CallsignUpdate.as_view(), name='callsign-html-update'),
    path('<slug>/claim', CallsignClaimView.as_view(), name='callsign-html-claim'),
]
