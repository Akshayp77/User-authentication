from rest_framework.authtoken.models import Token
from .models import Emp,create_auth_token
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from app.serializer import EmpS
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

# Create your views here.
def index(request):
    return HttpResponse("Welcome to home page")

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 

class api(APIView):
    def get(self,request):
        x=Emp.objects.all()
        serializer=EmpS(x,many=True)
        j_d= JSONRenderer().render(serializer.data)
        return HttpResponse(j_d,content_type='application/json')
    
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @csrf_exempt
    def post(self,request):
        name=request.POST['nm']
        e_id=request.POST['id']
        salary=request.POST['sal']
        Emp.objects.create(name=name,e_id=int(e_id),salary=int(salary))
        return HttpResponse("Data Entered")
    #@api_view(['PUT',])
    def put(self,request):
        #import pdb; pdb.set_trace()
        data=request.data
        p=data['id']
        name=data['nm']
        e_id=data['e_id']
        salary=data['sal']
        x=Emp.objects.get(pk=p)
        x.name= name
        x.e_id= int(e_id)
        x.salary=int(salary)
        x.save()
        return HttpResponse("Data Updated")
    def delete(self,request): 
        data=request.data
        p=data['id']
        x=Emp.objects.get(pk=p)
        x.delete()
        return HttpResponse("Data deleted Successfully")

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
    @csrf_exempt
    def get(self,request):
        if request.method =='GET':
            username=request.GET['username']
            password=request.GET['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                token=Token.objects.get(user=user)
                return HttpResponse(token,"Login Successfully")
            else:
                return HttpResponse("Password or username is wrong.Try again")