from django.urls import path

from .views import CallsignDetailView

urlpatterns = [
    path('<slug>/', CallsignDetailView.as_view(), name='callsign-detail'),
]
