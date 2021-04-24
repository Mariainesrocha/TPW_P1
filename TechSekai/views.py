from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from TechSekai.forms import *


# Create your views here.
def home(request):
    content = default_content(RegisterDjangoUserForm(), LoginDjangoUserForm())
    return render(request, 'home.html', content)


def new_arrivals(request):
    products = Product.objects.all().order_by("id")[0:20]

    register_form = RegisterDjangoUserForm()
    login_form = LoginDjangoUserForm()
    content = {
        'user_form': register_form,
        'login_form': login_form,
        'products': products,
        'page': 'New Arrivals'
    }
    return render(request, 'new_hot_items.html', content)


def hot_deals(request):
    products = Product.objects.all().order_by("-qty_sold")[0:20]  # Apenas os {20} Produtos + vendidos

    register_form = RegisterDjangoUserForm()
    login_form = LoginDjangoUserForm()
    content = {
        'user_form': register_form,
        'login_form': login_form,
        'products': products,
        'page': 'Hot Deals'
    }
    return render(request, 'new_hot_items.html', content)

## TODO: REFACTOR JUNTAR VIEW HOT DEALS C NEW_ARRIVALS -> o codigo é o mm
## TODO: NO BOTAO DE SEARCH TEM 'X' PRA APAGAR PESQUISA, DESCOBRIR ONDE ESTÁ E DAR REDIRECT PARA HOME


def search(request):
    name = request.GET['name']
    category = request.GET['category']
    products = Product.objects.filter(name__icontains=name, category__name__icontains=category)

    register_form = RegisterDjangoUserForm()
    login_form = LoginDjangoUserForm()
    content = {
        'user_form': register_form,
        'login_form': login_form,
        'products': products,
        'name': name,
        'category': category,
    }
    return render(request, 'itemsList.html', content)


def register(request):  # Usando o Pop-Up do Pedro. Até funciona, mas precisa de ajustes em termos de feedback..
    register = False
    if request.method == 'POST':
        register_form = RegisterDjangoUserForm(data=request.POST)

        if register_form.is_valid():
            user = User()
            django_user = register_form.save()
            django_user.set_password(django_user.password)
            try:
                django_user.save()
                user.django_user = django_user
                user.save()
                registered = True  # Pode ser usado para dar feedback de <criaçao com sucesso> ao user
            except:  # If something fails
                django_user.delete()
                user.delete()
        else:
            print(register_form.errors)
    else:
        register_form = RegisterDjangoUserForm()

    login_form = LoginDjangoUserForm()
    content = default_content(register_form, login_form)
    return render(request, 'mainLayout.html', content)


def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                print("Disabled account")
        else:
            print("User does not exist")

    register_form = RegisterDjangoUserForm()
    login_form = LoginDjangoUserForm()
    content = default_content(register_form, login_form)
    return render(request, 'home.html', content)


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


def registerShop(request):  # copiado do registerUser..mas precisa de mts alteracoes
    register = False
    if request.method == 'POST':
        add_shop_form = AddShopForm(data=request.POST)

        if add_shop_form.is_valid():
            shop = Shop()
            django_user = add_shop_form.save()
            django_user.set_password(django_user.password)
            try:
                django_user.save()
                shop.django_user = django_user
                shop.save()
                registered = True
            except:  # If something fails
                django_user.delete()
                shop.delete()
        else:
            print(add_shop_form.errors)
    else:
        print("For some reason it is not a POST------------------------")

    content = default_content()
    return render(request, 'mainLayout.html', content)


def add_product(request):
    return render(request, 'itemsList.html')


def list_products(request): # A FUNCIONAR!!! PRECISA DE AJUSTES NOS DADOS E PRA SER VER MELHOR SE TÁ TUDO OKAY
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(email=request.user.email)
        items = Item.objects.filter(shop=loggedShop)
        return render(request, 'itemsList.html', {'products': items})
    else:
        return render(request, 'error.html')


def default_content(user_form, login_form):
    brands_list = Brand.objects.all()
    products = Product.objects.all()
    hot_deals = products.order_by("-qty_sold")[0:20]  # Apenas os {20} Produtos + vendidos
    new_arrivals = products.order_by("id")[0:20]  # Assumindo que o id é auto-incremented... > id => + recente
    shops_list = Shop.objects.filter(certified=True)
    categories = Category.objects.all().order_by("-totDevices")[0:6]  #6 categorias com mais produtos disponiveis

    content = {'user_form': user_form, 'login_form': login_form,
               'brands_list': brands_list, 'shops_list': shops_list,
               'hot_deals': hot_deals, 'new_arrivals': new_arrivals, 'categories': categories}
    return content


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







''' 
NOT USED TO BE ERASED

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
'''