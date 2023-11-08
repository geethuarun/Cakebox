from rest_framework import serializers

from cakebox.models import User,Cakes,CakeVarient,Carts

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["id","username","password","address","email","phone"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class CakeVarientSerializer(serializers.ModelSerializer):

    id=serializers.CharField(read_only=True)
    class Meta:
        model=CakeVarient
        exclude=("cake",)


class CakesSerializer(serializers.ModelSerializer):

    type_of_cake=serializers.SlugRelatedField(read_only=True,slug_field="type_of_cake")
    varients=CakeVarientSerializer(many=True,read_only=True)
    class Meta:
        model=Cakes
        fields="__all__"

class CartSerializer(serializers.ModelSerializer):
    cakevarient=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)

    class Meta:
        model=Carts
        fields=["cakevarient","user","status","date"]





    

