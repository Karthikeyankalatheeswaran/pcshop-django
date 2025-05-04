from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Profile,Review


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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }