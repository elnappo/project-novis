from django.urls import path

from .views import *


urlpatterns = [
    path('api/radius/auth', RadiusAuthView.as_view()),
]
