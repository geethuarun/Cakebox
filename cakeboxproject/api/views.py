from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions

from cakebox.models import Cakes,CakeVarient,Carts
from api.serializer import UserSerializer,CakesSerializer,CartSerializer

class UserCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
class CakesView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CakesSerializer
    model=Cakes
    queryset=Cakes.objects.all()
    @action(methods=["post"],detail=True)
    def cart_add(self,request,*args,**kwargs):
        vid=kwargs.get("pk")
        varient_obj=CakeVarient.objects.get(id=vid)
        user=request.user
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cakevarient=varient_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class CartsView(ViewSet):
        authentication_classes=[authentication.BasicAuthentication]
        permission_classes=[permissions.IsAuthenticated]
        def list(self,request,*args,**kwargs):
            qs=Carts.objects.filter(user=request.user)
            serializer=CartSerializer(qs,many=True)
            return Response(data=serializer.data)
        def destroy(self,request,*args,**kwargs):
            id=kwargs.get("pk")
            qs=Carts.objects.get(id=id).delete()
            return Response(data={"msg":"deleted"})



    