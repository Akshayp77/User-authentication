from django import http
from django.http.response import HttpResponse
from django.shortcuts import render
from re import T, findall
import requests
from bs4 import BeautifulSoup
import collections
import pymongo
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User,auth
from rest_framework.authtoken.models import Token



class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 

class scrap(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self,request):
        if request.method =='POST':
            username=request.POST['username']
            password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            url="https://news.ycombinator.com/"
            r=requests.get(url)
            htmlContent=r.content
            sp=BeautifulSoup(htmlContent,'html.parser')
            client=pymongo.MongoClient("mongodb://localhost:27017/")
            more=''  
            while more!=None:
                url="https://news.ycombinator.com/"
                if more!='':
                    url=url+more['href']
                r=requests.get(url)
                htmlContent=r.content
                sp=BeautifulSoup(htmlContent,'html.parser')
                t=sp.find_all('td',class_='subtext')
                for j in t:
                    n= j.find_all_next()
                    t1=j.findParent()
                    if j.find('span',class_='score') not in n:
                        e=t1.find_all_previous('span',class_='rank')
                        num=e[0].text
                        flag1=1
                        if len(num)==3:
                            num=int(num[0:2:])
                        else:
                            num=int(num[0:1:])
                lnk=sp.find_all('a',class_='storylink',href=True,text=False)
                site=sp.find_all('span',class_='sitestr')
                s_no=sp.find_all('span',class_='rank')
                by=sp.find_all('a',class_="hnuser")
                title=sp.find_all('a',class_='storylink')
                points=sp.find_all('span',class_="score")
                time=sp.find_all('span',class_="age")
                l=[]
                c={}
                if flag1==1:
                    points.insert(num-1,'0 points')
                    by.insert(num-1,'')
                else:
                    num=-1

                for i in range(len(s_no)):
                    c={}
                    n=s_no[i].text
                    n=n[0:len(n)-1]
                    c['S_no']=int(n)
                
                    c['title']=title[i].text
                    if 'item?id=' in lnk[i]['href']:
                        c['link']='https://news.ycombinator.com/'+lnk[i]['href']
                        #print(c['link'])
                    else:
                        c['link']=lnk[i]['href']
                    if '.PDF' in c['link']:
                        print(c['link'])
                    if i==num-1:
                        c['points']='0 points'
                        c["by"]=''
                    else:
                        c['points']=points[i].text
                        c['by']=by[i].text
                    c['time']=time[i].text
                    
                    db=client['scrap']
                    collection=db['meta_data']
                    collection.insert_one(c)
                    l=collection.find_one({"S_no":int(n)})
                    #print(l)
                    new_d={}
                    
                    new_d['p_id']=l['_id']
                    new_d['link']=l['link']
                    collection=db['discription']
                    collection.insert_one(new_d)
                    
                    
                more=sp.find('a',class_='morelink',href=True,text=False)
            token=Token.objects.get(user=user)
            print(token)
            return HttpResponse("DATA stored in database Successfully")
        else:
            return HttpResponse("Username or Password is incorrect")
