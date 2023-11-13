from rest_framework import serializers

from cakebox.models import User,Cakes,CakeVarient,Carts,Order,Reviews,Offer

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["id","username","password","address","email","phone"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class OfferSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    price=serializers.CharField(read_only=True)
    start_date=serializers.CharField(read_only=True)
    end_date=serializers.CharField(read_only=True)
    


    class Meta:
        model=Offer
        exclude=("cakevarient",)


class CakeVarientSerializer(serializers.ModelSerializer):

    id=serializers.CharField(read_only=True)
    offer=OfferSerializer(read_only=True,many=True)
    class Meta:
        model=CakeVarient
        exclude=("cake",)

class ReviewSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    cake=serializers.CharField(read_only=True)


    class Meta:
        model=Reviews
        fields="__all__"




class CakesSerializer(serializers.ModelSerializer):

    type_of_cake=serializers.SlugRelatedField(read_only=True,slug_field="type_of_cake")
    varients=CakeVarientSerializer(many=True,read_only=True)
    reviews=ReviewSerializer(many=True,read_only=True)
    avg_rating=serializers.CharField(read_only=True)
    class Meta:
        model=Cakes
        fields="__all__"



class CartSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    cakevarient=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)

    class Meta:
        model=Carts
        fields=["id","cakevarient","user","status","date"]

class OrderSerializer(serializers.ModelSerializer):
    
    id=serializers.CharField(read_only=True)
    cakevarient=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    order_date=serializers.CharField(read_only=True)
    delivery_date=serializers.CharField(read_only=True)


    class Meta:
        model=Order
        fields="__all__"




    

