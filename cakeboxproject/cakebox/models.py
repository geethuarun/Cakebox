from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.

class User(AbstractUser):
     phone=models.CharField(max_length=100,unique=True)
     address=models.CharField(max_length=200)

class Category(models.Model):
     type_of_cake=models.CharField(max_length=200,unique=True)
     is_active=models.BooleanField(default=True)

     def __str__(self):
          return self.type_of_cake
     
class Cakes(models.Model):
     flavour=models.CharField(max_length=200)
     
     image=models.ImageField(upload_to="images")
     type_of_cake=models.ForeignKey(Category,on_delete=models.CASCADE)
     @property
     def varients(self):
          qs=self.cakevarient_set.all()
          return qs
     @property
     def reviews(self):
          qs=self.reviews_set.all()
          return  qs
     @property
     def avg_rating(self):
          ratings=self.reviews_set.all().values_list("rating",flat=True)
          return sum(ratings)/len(ratings) if ratings else 0


     def __str__(self):
          return self.flavour

class CakeVarient(models.Model):
     cake=models.ForeignKey(Cakes,on_delete=models.CASCADE)
     option1=(("egg","egg"),
              ("eggless","eggless"))
     version=models.CharField(max_length=200,choices=option1,default="egg")
     option2=(("round","round"),
             ("heart","heart"))
     shape=models.CharField(max_length=200,choices=option2,default="round")
     options=((".5kg",".5kg"),
              ("1kg","1kg"),
              ("1.5kg","1.5kg"),
              ("2kg","2kg"))
     weight=models.CharField(max_length=200,choices=options,default="1kg")
     price=models.PositiveIntegerField()

     def __str__(self):
          return self.cake.flavour 
     
     def offer(self):
          current_date=date.today()
          qs=self.offer_set.all()
          qs=qs.filter(end_date__gte=current_date)
          return qs
     

class Offer(models.Model):
     cakevarient=models.ForeignKey(CakeVarient,on_delete=models.CASCADE)
     price=models.PositiveIntegerField()
     start_date=models.DateTimeField()
     end_date=models.DateTimeField()

class Carts(models.Model):
     cakevarient=models.ForeignKey(CakeVarient,on_delete=models.DO_NOTHING)
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     options=(("in-cart","in-cart"),
              ("order placed","order placed"),
              ("cancelled","cancelled"))
     status=models.CharField(max_length=200,choices=options,default="in-cart")
     date=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
     cakevarient=models.ForeignKey(CakeVarient,on_delete=models.CASCADE)
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     options=(("order placed","order placed"),
              ("cancelled","cancelled"),
              ("dispatched","dispatched"),
              ("in-transit","in-transit"),
              ("deliverd","deliverd"))
     status=models.CharField(max_length=200,choices=options,default="order placed")
     order_date=models.DateTimeField(auto_now_add=True)
     delivery_date=models.DateTimeField(null=True)
     address=models.CharField(max_length=200)

from django.core.validators import MinValueValidator,MaxValueValidator

class Reviews(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     cake=models.ForeignKey(Cakes,null=True,on_delete=models.SET_NULL)
     rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
     comment=models.CharField(max_length=300)
     
     


     
     
     




