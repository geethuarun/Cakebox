from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,ListView,CreateView
from django.urls import reverse_lazy
from django.contrib import messages


from cakebox.models import User
from cakebox.forms import RegistrationForm

# Create your views here.

class SignUpView(CreateView):
    template_name="cakebox/register.html"
    form_class=RegistrationForm
    model=User
    success_url=reverse_lazy("signup")

    def form_valid(self, form):
        messages.success(self.request,"Account created successfully ")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Failed to create account")
        return super().form_invalid(form)
