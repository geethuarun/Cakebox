from django.urls import path
from cakebox.views import SignUpView,SignInView,CategoryView



urlpatterns=[
    path("register/",SignUpView.as_view(),name="signup"),
    path("",SignInView.as_view(),name="signin"),
    path("category/add",CategoryView.as_view(),name="add-category")
    
]