from django.urls import path

from .views import *


urlpatterns = [
    path('auth', RadiusAuthView.as_view()),
]
