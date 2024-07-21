from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    CAT=((1,'Pizza'),(2,'Burger'),(3,'Meal'),(4,'Cold Drinks'))
    name=models.CharField(max_length=20,verbose_name='Product Name')
    pdetail=models.CharField(max_length=100,verbose_name='Product Details')
    cat=models.IntegerField(verbose_name='Catagory',choices=CAT)
    price=models.IntegerField()
    is_active=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to='image')

class Cart(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    amt=models.IntegerField()

