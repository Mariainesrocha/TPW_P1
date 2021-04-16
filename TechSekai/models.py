from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import models as auth_models

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

ORDER_STATE = [
    ('ORDERED', 'Processing order'),
    ('DISPATCHED', 'Sent to delivery'),
    ('IN TRANSIT', 'On the way'),
    ('DELIVERED', 'Delivered at the destination address'),
    ('REFUND', 'Pay back to a non satisfied client'),
    ('FAILED', 'Error with the destination address, must contact us')
]

PAYMENT_METHOD = [
    ('Credit Card', 'Credit Card'),
    ('PayPal', 'PayPal'),
    ('ATM ', 'ATM')
]


class Address(models.Model):
    country = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    zip_code = models.CharField(max_length=10, null=False)
    street = models.CharField(max_length=100)
    door = models.IntegerField()
    floor = models.IntegerField()


class User(models.Model):
    django_user = models.OneToOneField(auth_models.User, on_delete=models.CASCADE)  #TODO: CONFIRMAR!!!!!!!!!!!!!!!!
    email = models.EmailField(max_length=35, primary_key=True, null=False)  #nota: tag primary_key define que esta é a PK e não um id
    name = models.CharField(max_length=40, null=False)
    gender = models.CharField(choices=GENDER, max_length=20)
    age = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(100), MinValueValidator(1)])
    phone_number = models.PositiveBigIntegerField()
    profile_pic = models.ImageField()
    role = models.CharField(max_length=10, choices=ROLES)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Shop(models.Model):
    name = models.CharField(max_length=40, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=35, null=False, primary_key=True)
    phone_number = models.PositiveBigIntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    website = models.URLField(max_length=40)
    opening_hours = models.TimeField(null=True)
    certified = models.BooleanField(null=False)
    image = models.ImageField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, primary_key=True)
    totDevices = models.IntegerField()


class Brand(models.Model):
    brand = models.CharField(max_length=50)


class Product(models.Model):
    reference_number = models.PositiveBigIntegerField(null=False)
    name = models.CharField(max_length=50, null=False)
    details = models.TextField(max_length=300)
    warehouse = models.CharField(max_length=50, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)


class Item(models.Model):
    price = models.PositiveIntegerField(null=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


class Cart(models.Model):
    quantity = models.PositiveIntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    total_price = models.PositiveIntegerField(null=False)


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)


class Order(models.Model):
    quantity = models.PositiveIntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    total_price = models.PositiveIntegerField(null=False)
    order_state = models.CharField(max_length=20, choices=ORDER_STATE)
    payment_meth = models.CharField(max_length=20, choices=PAYMENT_METHOD)


################################## LINKS Q PODEM VIR A SER UTEIS
'''
https://stackoverflow.com/questions/28712848/composite-primary-key-in-django
https://realpython.com/manage-users-in-django-admin/#model-permissions
https://docs.djangoproject.com/en/dev/ref/django-admin/#sqlclear-appname-appname
'''