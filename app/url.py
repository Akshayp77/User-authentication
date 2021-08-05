from django.contrib import admin
from django.urls import path,include
from . import views
from .views import user_auth_api,login,show


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('auth',user_auth_api.as_view()),
    path('login',login.as_view()),
    path('show',show.as_view())

]