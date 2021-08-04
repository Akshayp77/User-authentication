from django.db import models
from django.db.models.base import Model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Emp(models.Model):
    name=models.CharField(max_length=50)
    e_id=models.IntegerField()
    salary=models.IntegerField()

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**Kwargs):
    if created:
        Token.objects.create(user=instance)