from django import forms
# from .models import AuthWrapper, User, BaseLocation
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate
from .models import Account
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

#/***************************************************************************************
#*  REFERENCES
#*  Title: Real-time Chat Messenger (only for account and friends system)
#*  Author: CodingWithMitch
#*  Date: Oct 16th, 2020
#*  URL: https://www.youtube.com/playlist?list=PLgCYzUzKIBE9KUJZJUmnDFYQfVyXYjX6r
#*
#***************************************************************************************/

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', 'profile_image')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('status',)
    
    def save(self, user_id):
        print(self)
        account = Account.objects.get(pk=user_id)
        print(account)
        account.status = self.cleaned_data['status']
        account.save()
        return account

class UpdateLocationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('homeLongitude', 'homeLatitude')
    def save(self, user_id):
        print(self)
        account = Account.objects.get(pk=user_id)
        print(account)
        account.homeLongitude = self.cleaned_data['homeLongitude']
        account.homeLatitude = self.cleaned_data['homeLatitude']
        account.save()
        return account


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        if commit:
            account.save()
        return account