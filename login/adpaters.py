from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from allauth.account.signals import user_signed_up, password_set, user_logged_in, user_logged_out 
from allauth.account.adapter import DefaultAccountAdapter

class AuthAdapter(DefaultAccountAdapter):
    #Might need commit=False in **kwargs 
    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.savedLocations = ArrayField(models.CharField(max_length=200))        
        user.save()
        return user