from django import forms
from django.forms import ModelForm
from TechSekai.models import *


class CreateAccount(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    name = forms.CharField(label="Name", max_length=40)
    gender = forms.ChoiceField(label="Gender", choices=GENDER)
    phone_number = forms.IntegerField(label="Contact")


class AddAddressForm(forms.Form):
    country = forms.CharField(label='Country', max_length=50)
    city = forms.CharField(label='City', max_length=50)
    street = forms.CharField(label='Street', max_length=100)
    zip_code = forms.CharField(label='Zip Code', max_length=10)
    floor = forms.IntegerField(label='Floor')
    door = forms.IntegerField(label='Door')


class EditAccount(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'gender', 'phone_number', 'age', 'profile_pic']


class EditAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class AddShopForm(forms.Form):
    name = forms.CharField(label='Shop Name', max_length=40)
    owner = forms.CharField(label='Owner', max_length=40)
    email = forms.EmailField(label='Shop email', max_length=35)
    phone_number = forms.IntegerField(label='Contact')
    website = forms.URLField(label='Website URL', max_length=40)
    opening_hours = forms.TimeField(label='Opening hours')
    #certified = forms.BooleanField() #TODO ??????????????????????????????????? ISTO É SUPOSTO ESTAR SO EDITAVEL? SO PRA ADMIN?? HOW?
    image = forms.ImageField(label='Shop/Brand picture')


class EditShopForm(ModelForm):
    class Meta:
        model = Shop
        exclude = ['email']
        fields = '__all__'


class AddProductForm(forms.Form):
    reference_num = forms.IntegerField(label='Reference Number')
    name = forms.CharField(label='Product Name', max_length=50)
    details = forms.TextField('Details', max_length=300)
    warehouse = forms.CharField(label='Warehouse', max_length=50)

    category = forms.CharField(label='Category', max_length=50)    #TODO: NAO ESQUECER Q É FK LOGO TEMOS Q CRIAR OBJETO CATEGORY 1º E SÓ DPS PRODUCT (LOGICA DO LADO DA VIEWx)
    brand = forms.CharField(label='Brand', max_length=50)
    price = forms.IntegerField(label='Price') #com este campo do form, o produto em si e a loja "loggada" criamos o ITEM


class EditProductForm(forms.Form):
    class Meta:
        model = Shop
        exclude = ['reference_number']
        fields = '__all__'
