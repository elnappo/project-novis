from django.urls import path, include

from .views import UserUpdate, UserValidationView


urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/change', UserUpdate.as_view(), name="profile_change"),
    path('profile/validation', UserValidationView.as_view(), name="profile_validation"),
]
