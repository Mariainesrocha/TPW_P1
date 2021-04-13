from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

GENDER = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other/Not specified')
]

ROLES = [
    ('A', 'Admin'),
    ('C', 'Client'),
    ('S', 'Shop')
]

ORDER_STATE = [ #TODO: VER CODIGOS A APLICAR
    ('PROC', 'Processing order'),
    ('DELIV', 'Sent to delivery'),
    ('SENT', 'On its way'),
    ('REC', 'Delivered at the address')
]

PAYMENT_METHOD = [
    ('Credit Card', 'Credit Card'),
    ('PayPal', 'PayPal')
]


class Address(models.Model):
    country = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    zip_code = models.CharField(max_length=10, null=False)
    street = models.CharField(max_length=100)
    door = models.IntegerField()
    floor = models.IntegerField()


class User(models.Model):
    email = models.EmailField(max_length=35, primary_key=True, null=False)  #nota: tag primary_key define que esta é a PK e não um id
    name = models.CharField(max_length=40, null=False)
    gender = models.CharField(choices=GENDER, max_length=20)
    age = models.PositiveIntegerField(max_length=3, null=False, validators=[MaxValueValidator(100), MinValueValidator(1)])  #TODO: LIMITAR PRA MAIORES DE 16???
    phone_number = models.PositiveIntegerField(max_length=16)
    role = models.CharField(max_length=10,choices=ROLES)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    
class Shop(models.Model):
    name = models.CharField(max_length=40, null=False)
    owner = models.CharField(max_length=40, null=False)
    email = models.EmailField(max_length=35)
    phone_number = models.PositiveIntegerField(max_length=16)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    website = models.URLField(max_length=40)
    opening_hours = models.TimeField()
    certified = models.BooleanField(null=False)


class Category(models.Model):
    name = models.CharField(max_length=50, null=False)
    totDevices = models.IntegerField()


class Product(models.Model):
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null=False)
    details = models.TextField(max_length=300)
    warehouse = models.CharField(max_length=50, null=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)


class Item(models.Model):
    price = models.PositiveIntegerField(null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


class Cart(models.Model):
    quantity = models.PositiveIntegerField(max_length=5, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(null=False)


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Order(models.Model):
    quantity = models.PositiveIntegerField(max_length=5, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(null=False)
    order_state = models.CharField(max_length=20, choices=ORDER_STATE)
    payment_meth = models.CharField(max_length=20, choices=PAYMENT_METHOD)

