from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,ListView,CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


from cakebox.models import User,Category
from cakebox.forms import RegistrationForm,LoginForm,CategoryAddForm

# Create your views here.

class SignUpView(CreateView):
    template_name="cakebox/register.html"
    form_class=RegistrationForm
    model=User
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"Account created successfully ")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Failed to create account")
        return super().form_invalid(form)
    
class SignInView(FormView):
    template_name="cakebox/login.html"
    form_class=LoginForm
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login successfully ")
                return redirect("signin")
            else:
                messages.error(request,"invalid credentials")
                return render(request,self.template_name,{"form":form})
            
class CategoryView(CreateView,ListView):
    template_name="cakebox/category.html"
    model=Category
    form_class=CategoryAddForm
    context_object_name="categories"
    success_url=reverse_lazy("add-category")
    def form_valid(self, form):
        messages.success(self.request,"category added successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"category adding failed")
        return super().form_invalid(form)

