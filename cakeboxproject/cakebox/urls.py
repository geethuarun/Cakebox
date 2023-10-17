from django.urls import path
from cakebox.views import SignUpView,SignInView,CategoryView,remove_category,CakeCreateView,\
CakeListView,CakeUpdateView,remove_cakeview,CakeVarientView



urlpatterns=[
    path("register/",SignUpView.as_view(),name="signup"),
    path("",SignInView.as_view(),name="signin"),
    path("categories/add",CategoryView.as_view(),name="add-category"),
    path("categories/<int:pk>/remove",remove_category,name="remove-category"),
    path("cakes/add",CakeCreateView.as_view(),name="cake-add"),
    path("cakes/all",CakeListView.as_view(),name="cake-list"),
    path("cakes/<int:pk>/change",CakeUpdateView.as_view(),name="cake-change"),
    path("cakes/<int:pk>/remove",remove_cakeview,name="cake-remove"),
    path("cake/<int:pk>/varients/add",CakeVarientView.as_view(),name="add-varient")
    
]