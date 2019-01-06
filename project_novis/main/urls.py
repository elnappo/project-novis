from django.urls import path
from django.contrib.flatpages import views

from .views import HomePageView, EmptyView, VersionView, RobotsView

urlpatterns = [
    path('', HomePageView.as_view(), name="index"),
    path('version', VersionView.as_view(), name="version"),
    path('healthz', EmptyView.as_view(), name="healthz"),
    path('readiness', EmptyView.as_view(), name="readiness"),
    path('robots.txt', RobotsView.as_view(), name="robots"),

    # Flatpages
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('privacy/', views.flatpage, {'url': '/privacy/'}, name='privacy'),
    path('contact/', views.flatpage, {'url': '/contact/'}, name='contact'),
    path('contrib/', views.flatpage, {'url': '/contrib/'}, name='contrib'),
    path('help/', views.flatpage, {'url': '/help/'}, name='help'),
]
