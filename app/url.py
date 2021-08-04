from django.contrib import admin
from django.urls import path,include
from . import views
from .views import user_auth_api,api


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('auth',user_auth_api.as_view()),
    path('api',api.as_view())
]