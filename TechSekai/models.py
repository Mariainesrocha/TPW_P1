from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import models as auth_models
from django.db.models import UniqueConstraint

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
    UniqueConstraint(fields=['street', 'door', 'floor'], name='unique_address')

    def __str__(self):
        return self.street + " Nº " + str(self.door) + " " + str(self.floor) + " ; " + self.zip_code + " , " + self.city + " (" + self.country + ")"


class User(models.Model):
    django_user = models.OneToOneField(auth_models.User, on_delete=models.CASCADE)

    gender = models.CharField(choices=GENDER, max_length=20, null=True, blank=True)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], null=True, blank=True)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='images/')
    role = models.CharField(max_length=10, choices=ROLES, null=True, blank=True)    ## TODO: REMOVER ISTO NE?
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    # to return a meaningful value when a unicode representation of a User model instance is requested.(?)
    # See more: https://www.tangowithdjango.com/book/chapters/login.html
    def __unicode__(self):
        return self.django_user.username

    def __str__(self):
        return self.django_user.username


class Shop(models.Model):
    name = models.CharField(max_length=40, null=False)
    owner = models.OneToOneField(auth_models.User, on_delete=models.CASCADE) #TODO: DESCOMENTAR
    phone_number = models.PositiveBigIntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    website = models.URLField(max_length=40, null=True)
    opening_hours = models.TimeField(null=True)
    certified = models.BooleanField(null=False)
    image = models.ImageField(null=True, upload_to='images/')

    def __str__(self):
        return self.name + " , " + self.owner.username


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, primary_key=True)
    totDevices = models.IntegerField()
    image = models.ImageField(null=True, default='images/logo.png', upload_to='images/')

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    reference_number = models.PositiveBigIntegerField(null=False)
    name = models.CharField(max_length=50, null=False)
    details = models.TextField(max_length=300)
    warehouse = models.CharField(max_length=50, null=False)
    qty_sold = models.IntegerField()
    image = models.ImageField(null=True, default='logo.png', upload_to='images/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    lowest_price = models.IntegerField(null=False, default=0)

    UniqueConstraint(fields=['reference_number', 'brand', 'name'], name='unique_product')

    def __str__(self):
        return " [ " + str(self.reference_number) + " ] " + self.name + ", " + self.brand.name


class Item(models.Model):
    price = models.PositiveIntegerField(null=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
        return self.product.name + " price: " + str(self.price)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
        return self.user.django_user.username + ", total_price: " + str(self.total_price)


class Cart_Item(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(null=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.product.name + " , "+self.cart.user.django_user.username


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prods = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.django_user.username + ", num_items: " + str(len(self.prods.all()))


class Order(models.Model):
    quantity = models.PositiveIntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(null=False)
    order_state = models.CharField(max_length=20, choices=ORDER_STATE)
    payment_meth = models.CharField(max_length=20, choices=PAYMENT_METHOD)

    def __str__(self):
        return self.user.django_user.first_name


################################## LINKS Q PODEM VIR A SER UTEIS
'''
https://realpython.com/manage-users-in-django-admin/#model-permissions
'''
