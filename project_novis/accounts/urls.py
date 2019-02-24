from django.urls import path, include

from .views import UserUpdate, UserSocialUpdate, UserValidationView


urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/change', UserUpdate.as_view(), name="profile_change"),
    path('profile/social/change', UserSocialUpdate.as_view(), name="profile_social_change"),
    path('profile/validation', UserValidationView.as_view(), name="profile_validation"),
]
