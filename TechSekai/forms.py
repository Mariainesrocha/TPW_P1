from django import forms
from django.forms import ModelForm
from TechSekai.models import *
from django.contrib.auth import models
from django.core.validators import RegexValidator


class RegisterDjangoUserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class LoginDjangoUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=40, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))


class EditUserForm(forms.Form):  # Used in Account_Page View
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Username", max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))

    gender = forms.ChoiceField(label="Gender", choices=GENDER, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.IntegerField(validators=[phone_regex], label="Contact", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(label="Age", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(label="Avatar", required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))


class SearchForm(forms.Form):
    name = forms.CharField(max_length=40)


class AddAddressForm(forms.Form):
    country = forms.CharField(label='Country', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(label='City', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    street = forms.CharField(label='Street', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    zip_code = forms.CharField(label='Zip Code', max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    floor = forms.IntegerField(label='Floor', widget=forms.NumberInput(attrs={'class':'form-control'}))
    door = forms.IntegerField(label='Door', widget=forms.NumberInput(attrs={'class':'form-control'}))


class EditAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'door': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AddItem(ModelForm):
    class Meta:
        model = Item
        exclude = ('shop',)
        fields = '__all__'


class EditItem(ModelForm):
    class Meta:
        model = Item
        exclude = ('shop',)
        fields = '__all__'


class AddShopForm(forms.Form):
    name = forms.CharField(label='Shop Name', max_length=40, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.IntegerField(validators=[phone_regex], label='Shop Phone Number', widget=forms.TextInput(attrs={'class':'form-control'}))


class EditShopForm(ModelForm):
    class Meta:
        model = Shop
        exclude = ['certified', 'address', 'owner']
        fields = '__all__'
        widgets = {
            'opening_hours': forms.TimeInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditDjangoUserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddProductForm(forms.Form):
    reference_num = forms.IntegerField(label='Reference Number', widget=forms.NumberInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Product Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    details = forms.CharField(label='Details', max_length=300, required=False, widget=forms.Textarea(attrs={'class':'form-control'}))
    warehouse = forms.CharField(label='Warehouse', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(label='Product image', required=False)
    price = forms.IntegerField(label='Price', widget=forms.NumberInput(attrs={'class':'form-control'}))

    category = forms.ModelChoiceField(label='Category', queryset=Category.objects.all().order_by('name'))
    new_cat = forms.CharField(label='Other category', max_length=50, required=False, disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    brand = forms.ModelChoiceField(label='Brand', queryset=Brand.objects.all().order_by('name'))
    new_brand = forms.CharField(label='Other brand',  required=False, max_length=50, disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))


class EditProductForm(ModelForm):
    new_cat = forms.CharField(label='Other category', max_length=50, required=False, disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    new_brand = forms.CharField(label='Other brand',  required=False, max_length=50, disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.IntegerField(label='Price', widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Product
        exclude = ['reference_number', 'qty_sold', 'lowest_price', 'creator']
        fields = '__all__'


class DoOrderForm(forms.Form):
    qty = forms.IntegerField(label="Quantity", widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_meth = forms.ChoiceField(label="Payment Method", choices=PAYMENT_METHOD, widget=forms.Select(attrs={'class': 'form-control'}))


class CartBuyForm(forms.Form):
    payment_meth = forms.ChoiceField(label="Payment Method", choices=PAYMENT_METHOD,widget=forms.Select(attrs={'class': 'form-control'}))