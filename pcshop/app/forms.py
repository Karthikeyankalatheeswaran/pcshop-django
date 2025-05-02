from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'address']
        
        
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['phone_number', 'address', 'pin_code']