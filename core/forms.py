from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from core.services.user import UserService

from .models import User
        
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils import timezone



class RegistrationForm(forms.ModelForm):
   #  password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if user.is_staff is None:
            user.is_staff = False
        if user.is_active is None:
            user.is_active = True
        if user.date_joined is None:
            user.date_joined = timezone.now()
        if commit:
            user.save()
            UserService.create_cart_data(user)
        return user


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if user.is_staff is None:
            user.is_staff = False
        if user.is_active is None:
            user.is_active = True
        if user.date_joined is None:
            user.date_joined = timezone.now()
        
        if commit:
            user.save()
            UserService.create_cart_data(user)
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
