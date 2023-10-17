from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,ListView,CreateView,UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


from cakebox.models import User,Category,Cakes,CakeVarient
from cakebox.forms import RegistrationForm,LoginForm,CategoryAddForm,CakeAddForm,CakeVarientForm

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
    def get_queryset(self):
        return Category.objects.filter(is_active=True)

def remove_category(request,*args,**kwargs):
    id=kwargs.get("pk")
    Category.objects.filter(id=id).update(is_active=False)
    messages.success(request,"category removed")
    return redirect("add-category")

class CakeCreateView(CreateView):
    template_name="cakebox/cake_add.html"
    model=Cakes
    form_class=CakeAddForm
    success_url=reverse_lazy("cake-add")
    def form_valid(self, form):
        messages.success(self.request,"cake added")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"cake adding failed")
        return super().form_invalid(form)
    
class CakeListView(ListView):
    template_name="cakebox/cake_list.html"
    model=Cakes
    context_object_name="cakes"

class CakeUpdateView(UpdateView):
    template_name="cakebox/cake_edit.html"
    form_class=CakeAddForm
    model=Cakes
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        messages.success(self.request,"Cake updated successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Cake updating failed")
        return super().form_invalid(form)
    

def remove_cakeview(request,*args,**kwargs):
    id=kwargs.get("pk")
    Cakes.objects.filter(id=id).delete()
    return redirect("cake-list")


class CakeVarientView(CreateView):
    template_name="cakebox/cakevarient_add.html"
    form_class=CakeVarientForm
    model=CakeVarient
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        messages.success(self.request,"cakevarient added")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"cakevarient adding failed")
        return super().form_invalid(form)
    

