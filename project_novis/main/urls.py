from django.urls import path
from django.contrib.flatpages import views

from .views import HomePageView, EmptyView, VersionView, RobotsView

urlpatterns = [
    path('', HomePageView.as_view(), name="index"),
    path('version', VersionView.as_view(), name="version"),
    path('healthz', EmptyView.as_view(), name="healthz"),  # Only for reference, handled in HealthCheckMiddleware
    path('readiness', EmptyView.as_view(), name="readiness"),  # Only for reference, handled in HealthCheckMiddleware
    path('robots.txt', RobotsView.as_view(), name="robots"),

    # Flatpages
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('privacy/', views.flatpage, {'url': '/privacy/'}, name='privacy'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
    path('contrib/', views.flatpage, {'url': '/contrib/'}, name='contrib'),
]
