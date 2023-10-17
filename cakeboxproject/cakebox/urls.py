from django.urls import path
from cakebox.views import SignUpView,SignInView,CategoryView,remove_category,CakeCreateView,\
CakeListView,CakeUpdateView,remove_cakeview,CakeVarientView,CakeDetailView,CakeVarientUpdateView,\
remove_varient,OfferCreateView



urlpatterns=[
    path("register/",SignUpView.as_view(),name="signup"),
    path("",SignInView.as_view(),name="signin"),
    path("categories/add",CategoryView.as_view(),name="add-category"),
    path("categories/<int:pk>/remove",remove_category,name="remove-category"),
    path("cakes/add",CakeCreateView.as_view(),name="cake-add"),
    path("cakes/all",CakeListView.as_view(),name="cake-list"),
    path("cakes/<int:pk>/change",CakeUpdateView.as_view(),name="cake-change"),
    path("cakes/<int:pk>/remove",remove_cakeview,name="cake-remove"),
    path("cakes/<int:pk>/varients/add",CakeVarientView.as_view(),name="add-varient"),
    path("cakes/<int:pk>/",CakeDetailView.as_view(),name="cake-detail"),
    path("varients/<int:pk>/change",CakeVarientUpdateView.as_view(),name="varient-change"),
    path("varient/<int:pk>/remove",remove_varient,name="remove-varient"),
    path("varient/<int:pk>/offer/add",OfferCreateView.as_view(),name="offers-add")
    
]