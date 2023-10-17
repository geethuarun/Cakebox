from django import forms
from django.contrib.auth.forms import UserCreationForm
from cakebox.models import User,Category,Cakes,CakeVarient,Offer

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2","phone","address"]


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class CategoryAddForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=["type_of_cake"]

class CakeAddForm(forms.ModelForm):
    class Meta:
        model=Cakes
        fields="__all__"

class CakeVarientForm(forms.ModelForm):
    class Meta:
        model=CakeVarient
        exclude=("cake",)

class OfferForm(forms.ModelForm):
    class Meta:
        model=Offer
        exclude=("cakevarient",)
        widgets={"start_date":forms.DateInput(attrs={"type":"date"}),
                "end_date":forms.DateInput(attrs={"type":"date"}) }