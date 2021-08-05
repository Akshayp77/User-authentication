from django.contrib import admin
from django.urls import path
from . import views
from data.views import scrap

urlpatterns = [
    path('scrap',scrap.as_view())
]