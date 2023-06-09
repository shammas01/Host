from sys import setprofile
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from . models import Customer
from django.core.validators import EmailValidator


from django.core.mail import send_mail
from django.conf import settings
import random



class CustomerRegistration(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter-Username'}))    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not any(char.isalpha() for char in username):
            raise forms.ValidationError('Username must contain at least one alphabetic character.')
        if sum(char.isdigit() for char in username) < 0:
            raise forms.ValidationError('')
        if username.isdigit():
            raise forms.ValidationError('Username cannot contain numbers only.')
        return username
    
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Enter Password'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Re-enter Password'}))    
    
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={'placeholder': 'Email address','class':'form-control'}),
        required=True
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please choose a different email.")
        return email
    
    
    # def send_otp_email(self, email, otp):
    #     subject = 'Your OTP for registration'
    #     message = f'Your OTP for registration is: {otp}'
    #     from_email = settings.DEFAULT_FROM_EMAIL
    #     recipient_list = [email]
    #     send_mail(subject, message, from_email, recipient_list)

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.is_active = False  # deactivate the user until they verify their OTP
    #     if commit:
    #         user.save()
    #     return user
    
    
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        





class LoginForm(AuthenticationForm):
    
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
            
    # def _init_(self, *args, **kwargs):
    #     super()._init_(*args, **kwargs)
    #     self.fields['Old_password'], self.fields['New_password'],self.fields['Confirm_password']
    #     # self.fields['email'], self.fields['password1']
    #     del self.fields['old_password'], self.fields['new_password1'],self.fields['new_password2']
    



class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['id','name','locality','city','state','mobile','zipcode']
        
        widgets ={
            
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),   
        }


    

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'Current Password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'autocomplete':'Current Password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'autocomplete':'Current Password','class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))




    
    
            