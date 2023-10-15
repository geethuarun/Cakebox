from django.urls import path
from cakebox.views import SignUpView



urlpatterns=[
    path("register/",SignUpView.as_view(),name="signup")
    
]