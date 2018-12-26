from django.urls import path, re_path

from .views import CallSignDetailView, CallSignCreate, CallSignUpdate, CallSignClaimView, CallSignSearchView

app_name = "callsign"

urlpatterns = [
    path('add/', CallSignCreate.as_view(), name='callsign-html-create'),
    path('<slug>/', CallSignDetailView.as_view(), name='callsign-html-detail'),
    path('<slug>/change', CallSignUpdate.as_view(), name='callsign-html-update'),
    path('<slug>/claim', CallSignClaimView.as_view(), name='callsign-html-claim'),
    path('search', CallSignSearchView.as_view(), name='callsign-html-search'),
]
