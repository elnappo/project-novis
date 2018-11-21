from django.urls import path

from .views import HomePageView, EmptyView, VersionView, RobotsView

urlpatterns = [
    path('', HomePageView.as_view(), name="index"),
    path('version', VersionView.as_view(), name="version"),
    path('healthz', EmptyView.as_view(), name="healthz"),
    path('readiness', EmptyView.as_view(), name="readiness"),
    path('robots.txt', RobotsView.as_view(), name="robots"),
]
