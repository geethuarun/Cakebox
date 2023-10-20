from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,ListView,CreateView,UpdateView,DetailView,TemplateView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator


from cakebox.models import User,Category,Cakes,CakeVarient,Offer
from cakebox.forms import RegistrationForm,LoginForm,CategoryAddForm,CakeAddForm,CakeVarientForm,OfferForm

# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
def is_admin(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            messages.error(request,"permission denied for current user")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,is_admin]   


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
                return redirect("index")
            else:
                messages.error(request,"invalid credentials")
                return render(request,self.template_name,{"form":form})

@method_decorator(decs,name="dispatch")            
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

@signin_required
@is_admin
def remove_category(request,*args,**kwargs):
    id=kwargs.get("pk")
    Category.objects.filter(id=id).update(is_active=False)
    messages.success(request,"category removed")
    return redirect("add-category")

@method_decorator(decs,name="dispatch")
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

@method_decorator(decs,name="dispatch")    
class CakeListView(ListView):
    template_name="cakebox/cake_list.html"
    model=Cakes
    context_object_name="cakes"

@method_decorator(decs,name="dispatch")
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
    
@signin_required
@is_admin
def remove_cakeview(request,*args,**kwargs):
    id=kwargs.get("pk")
    Cakes.objects.filter(id=id).delete()
    return redirect("cake-list")

@method_decorator(decs,name="dispatch")
class CakeVarientView(CreateView):
    template_name="cakebox/cakevarient_add.html"
    form_class=CakeVarientForm
    model=CakeVarient
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=Cakes.objects.get(id=id)
        form.instance.cake=obj
        messages.success(self.request,"cakevarient added")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"cakevarient adding failed")
        return super().form_invalid(form)

@method_decorator(decs,name="dispatch")    
class CakeDetailView(DetailView):
    template_name="cakebox/cake_detail.html"
    model=Cakes
    context_object_name="cake"

@method_decorator(decs,name="dispatch")
class CakeVarientUpdateView(UpdateView):
    template_name="cakebox/varient_edit.html"
    form_class=CakeVarientForm
    model=CakeVarient
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        messages.success(self.request,"cakevarient updated")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"cakevarient updating failed")
        return super().form_invalid(form)
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cake_varient_object=CakeVarient.objects.get(id=id)
        cake_id=cake_varient_object.cake.id
        return reverse("cake-detail",kwargs={"pk":cake_id})

@signin_required
@is_admin
def remove_varient(request,*args,**kwargs):
    id=kwargs.get("pk")
    CakeVarient.objects.filter(id=id).delete()
    return redirect("cake-list")

@method_decorator(decs,name="dispatch")
class OfferCreateView(CreateView):
    template_name="cakebox/offer_add.html"
    model=Offer
    form_class=OfferForm
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=CakeVarient.objects.get(id=id)
        form.instance.cakevarient=obj
        messages.success(self.request,"Offer hasbeen added successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Offer adding failed")
        return super().form_invalid(form)
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cake_varient_object=CakeVarient.objects.get(id=id)
        cake_id=cake_varient_object.cake.id
        return reverse("cake-detail",kwargs={"pk":cake_id})

@signin_required
@is_admin    
def delete_offer_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    offer_object=Offer.objects.get(id=id)
    cake_id=offer_object.cakevarient.cake.id
    offer_object.delete()
    return redirect("cake-detail",pk=cake_id)

@signin_required
def sign_out_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

class IndexView(TemplateView):
    template_name="cakebox/index.html"
        
    

