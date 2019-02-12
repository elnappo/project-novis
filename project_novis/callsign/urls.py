from django.urls import path

from .views import CallSignDetailView, CallSignCreate, CallSignUpdate, CallSignClaimView

app_name = "callsign"

urlpatterns = [
    path('add/', CallSignCreate.as_view(), name='callsign-html-create'),

    path('<slug>/', CallSignDetailView.as_view(), name='callsign-html-detail'),
    path('<slug>/change', CallSignUpdate.as_view(), name='callsign-html-update'),
    path('<slug>/claim', CallSignClaimView.as_view(), name='callsign-html-claim'),
]
