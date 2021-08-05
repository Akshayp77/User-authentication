from rest_framework.authtoken.models import Token
from .models import create_auth_token
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication

# Create your views here.

def index(request):
    return HttpResponse("Welcome to home page")

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 

class user_auth_api(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):
        if request.method=='POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            pass1=request.POST['password1']
            pass2=request.POST['password2']
            if pass1 !=pass2:
                return HttpResponse("password not matched")
            if User.objects.filter(username=username).exists():
                return HttpResponse("User already exist")
            else:
                user=User.objects.create_user(username=username,password=pass1,first_name=first_name,last_name=last_name)
                user.save()
                return HttpResponse("User registered")
class login(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):
        if request.method =='POST':
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                token=Token.objects.get(user=user)
                return HttpResponse(token,"Login Successfully")
            else:
                return HttpResponse("Password or username is wrong.Try again")
class show(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):

        if request.method=='POST':
            key=request.POST['token']
            try:
                x=Token.objects.get(key=key).user
            except:
                return HttpResponse("Incorrect Token!, you can not access this api")
            else:
                return HttpResponse("Hello "+str(x).capitalize())
        