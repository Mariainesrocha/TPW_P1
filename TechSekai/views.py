from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from TechSekai.forms import *


# Create your views here.
def home(request):
    user_form = RegisterDjangoUserForm()
    login_form = LoginDjangoUserForm()

    brands_list = Brand.objects.all()
    products = Product.objects.all()
    hot_deals = products.order_by("-qty_sold")[0:20] #Apenas os {20} Produtos + vendidos
    new_arrivals = products.order_by("id") #Assumindo que o id é auto-incremented... > id => + recente
    shops = Shop.objects.filter(certified=True)

    content = {'user_form': user_form, 'login_form': login_form,
               'brands_list': brands_list, 'shops_list': shops,
               'hot_deals': hot_deals, 'new_arrivals': new_arrivals}
    return render(request, 'home.html', content)


def top_seller(request):
    return render(request, 'TopSeller.html')


def new_arrival(request):
    return render(request, 'NewArrival.html')


def account_page(request):
    user = User.objects.get(django_user=request.user)
    updated = False
    if request.method == "POST":
        user_form = EditUserForm(request.POST)

        if user_form.is_valid():
            # Update All Fields
            user.django_user.username = user_form.cleaned_data['username']
            user.django_user.email = user_form.cleaned_data['email']
            user.phone_number = user_form.cleaned_data['phone_number']
            user.age = user_form.cleaned_data['age']
            user.gender = user_form.cleaned_data['gender']
            user.django_user.save()
            user.save()
            updated = True
        else:
            print(user_form.errors)

    # POST or not, we load the Known Values
    user_form = EditUserForm(initial={'username': user.django_user.username,
                                      'email': user.django_user.email,
                                      'phone_number': user.phone_number,
                                      'age': user.age,
                                      'gender': user.gender})

    return render(request, 'Account.html', {'extra_user_form': user_form, 'updated': updated})


def register(request): #Usando o Pop-Up do Pedro. Funcionar até funciona, mas precisa de ajustes em termos de feedback..
    if request.method == 'POST':
        user_form = RegisterDjangoUserForm(data=request.POST)

        if user_form.is_valid():
            user = User()
            django_user = user_form.save()
            django_user.set_password(django_user.password)
            try:
                django_user.save()
                user.django_user = django_user
                user.save()
                registered = True
            except:  # If something fails
                django_user.delete()
                user.delete()
        else:
            print(user_form.errors)
    else:
        user_form = RegisterDjangoUserForm()
        print("For some reason it is not a POST------------------------")

    user_form = RegisterDjangoUserForm()
    login_form = LoginDjangoUserForm()
    return render(request, 'home.html', {'user_form': user_form, 'login_form': login_form})

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            print("Disabled account")
    else:
        print("User does not exist")
    user_form = RegisterDjangoUserForm()
    login_form = LoginDjangoUserForm()
    return render(request, 'home.html', {'user_form': user_form, 'login_form': login_form})


def registerOLD(request):
    registered = False

    if request.method == 'POST':
        user_form = RegisterDjangoUserForm(data=request.POST)

        if user_form.is_valid():
            user = User()
            django_user = user_form.save()
            django_user.set_password(django_user.password)
            try:
                django_user.save()
                user.django_user = django_user
                user.save()
                registered = True
            except:  # If something fails
                django_user.delete()
                user.delete()
        else:
            print(user_form.errors)

    else:
        user_form = RegisterDjangoUserForm()

    return render(request, 'Register.html', {'user_form': user_form, 'registered': registered})


## TODO NOTA: USAR ISTO ANTES DE CADA VIEW Q NECESSITA DE LOGIN PARA GARANTIR CONTA É + FACIL
# @login_required(login_url='/accounts/login/') -> caso tenham duvidas: https://docs.djangoproject.com/en/3.1/topics/auth/default/

'''
# usar import:
from django.contrib.auth.decorators import user_passes_test


def email_check(user):
    return user.email.endswith('@example.com')

@user_passes_test(email_check)
def my_view(request):
'''
