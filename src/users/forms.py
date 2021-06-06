from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.hashers import check_password
from django.db import models
from django.db.models import fields

from users.models import NewUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100,help_text='Required. Add a valid email address')

    class Meta:
        model = NewUser
        fields = ('email','user_name','first_name','last_name','password1','password2','is_investor','company_name','company_code','company_site')
        

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ('email','password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login")

class CompanyUpdateForm (BSModalModelForm):
    class Meta:
        model = NewUser
        fields =('company_name','company_code','company_site')

class AccountUpdateForm(BSModalModelForm):
    email = forms.EmailField(max_length=100,help_text='Required. Add a valid email address')
    class Meta:
        model = NewUser
        fields =('email','user_name','first_name','last_name')


class PasswordConfirmationForm(BSModalModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = NewUser
        fields = ('confirm_password',)

    def clean(self):
        cleaned_data = super(PasswordConfirmationForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Password does not match.')
