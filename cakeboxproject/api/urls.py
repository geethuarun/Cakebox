from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("cakes",views.CakesView,basename="cakes")

router.register("carts",views.CartsView,basename="carts")


urlpatterns=[
    path("register/",views.UserCreationView.as_view())
    
]+router.urls