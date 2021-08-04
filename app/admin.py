from django.contrib import admin
from .models import Emp
from .serializer import EmpS


admin.site.register(Emp)