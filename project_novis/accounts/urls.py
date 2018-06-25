from django.urls import path, include

from .views import UserUpdate


urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/change', UserUpdate.as_view(), name="profile_change"),
]
