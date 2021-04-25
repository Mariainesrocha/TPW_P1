from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from TechSekai.forms import *


# Create your views here.
def home(request):
    content = default_content(request)
    return render(request, 'home.html', content)


def login_view(request):
    register_error = False
    login_error = False
    if request.method == "POST":
        if 'sign_in' in request.POST:
            login_form = LoginDjangoUserForm(data=request.POST)
            register_form = RegisterDjangoUserForm()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return render(request, 'home.html')
            else:
                print("User does not exist")
                login_error = True
        elif 'sign_up' in request.POST:
            register_form = RegisterDjangoUserForm(data=request.POST)
            login_form = LoginDjangoUserForm()
            if register_form.is_valid():
                print("valid")
                user = User()
                django_user = register_form.save()
                django_user.set_password(django_user.password)
                django_user.save()
                user.django_user = django_user
                cart = Cart(user=user)
                wishlist = WishList(user=user)
                user.save()
                cart.save()
                wishlist.save()
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                login(request, user)
                return render(request, 'home.html')

            else:
                print(register_form.errors)
                register_error = True

    else:
        register_form = RegisterDjangoUserForm()
        login_form = LoginDjangoUserForm()
    content = {'user_form': register_form, 'login_form': login_form, 'register_error': register_error,
               'login_error': login_error}
    return render(request, 'login.html', content)


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
    content = {
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
    content = {
        'products': products,
        'name': name,
        'category': category,
    }
    return render(request, 'itemsList.html', content)


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

    content = default_content(request)
    return render(request, 'mainLayout.html', content)


def add_product(request):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(email=request.user.email)
        if request.method == 'POST':
            form = AddProductForm(request.POST)

            if form.is_valid():
                reference_number = form.cleaned_data['reference_num']
                name = form.cleaned_data['name']
                details = form.cleaned_data['details']
                warehouse = form.cleaned_data['warehouse']
                price = form.cleaned_data['price']
                image = form.cleaned_data['image']
                category = form.cleaned_data['category']
                brand = form.cleaned_data['brand']

                # lowest_price = form.cleaned_data['lowest_price']
                if category == 'Other':
                    new_cat = form.cleaned_data['new_cat']
                    category = Category(name=new_cat, totDevices=0)
                    category.save()

                if category == 'Other':
                    form.new_cat.disabled = False
                    new_brand = form.cleaned_data['new_brand']
                    brand = Brand(name=new_brand)
                    brand.save()

                try:
                    p = Product(qty_sold=0, reference_number=reference_number, name=name, details=details,
                                warehouse=warehouse, image=image, category=category, brand=brand)
                    p.save()

                    c = Category.objects.get(name=category)
                    c.totDevices += 1
                    c.save()

                    i = Item(price=price, shop=loggedShop, product=p)
                    i.save()
                except:
                    return render(request, 'forms.html', {'msgErr': ' Product not inserted, try again later!'})
                return render(request, 'forms.html', {'msg': ' Product ' + p.name + ' inserted successfully!'})
        else:
            form = AddProductForm()
            return render(request, 'forms.html', {'form': form})
    else:
        return render(request, 'error.html')


def list_products(request):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(email=request.user.email)
        items = Item.objects.filter(shop=loggedShop)
        p = [i.product for i in items]
        return render(request, 'itemsList.html', {'products': p})
    else:
        return render(request, 'error.html')


def default_content(request):
    brands_list = cache.get('brands_list')
    hot_deals = cache.get('hot_deals')
    new_arrivals = cache.get('new_arrivals')
    shops_list = cache.get('shops_list')
    categories = cache.get('categories')
    if not (brands_list and hot_deals and new_arrivals and shops_list and categories):
        brands_list = Brand.objects.all()
        products = Product.objects.all()
        hot_deals = products.order_by("-qty_sold")[0:12]
        new_arrivals = products.order_by("id")[0:12]
        shops_list = Shop.objects.filter(certified=True)
        categories = Category.objects.all().order_by("-totDevices")[0:6]  # 6 categorias com mais produtos disponiveis

        cache.set('brands_list', brands_list)
        cache.set('products', products)
        cache.set('hot_deals', hot_deals)
        cache.set('new_arrivals', new_arrivals)
        cache.set('shops_list', shops_list)
        cache.set('categories', categories)

    return {'brands_list': brands_list, 'shops_list': shops_list,
            'hot_deals': hot_deals, 'new_arrivals': new_arrivals, 'categories': categories}


def product_shops(request, prod_id):
    product_in_wishlist = False
    product = Product.objects.get(id=prod_id)
    item_per_shop = Item.objects.filter(product=product)

    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_wishlist = WishList.objects.get(user=user)
        if product in user_wishlist.prods.all():
            product_in_wishlist = True

    return render(request, 'prod_Info.html',
                  {'prod': product, 'wishlist': product_in_wishlist, 'prod_per_shop': item_per_shop})


def order_product(request, item_id):
    if request.user.is_authenticated:
        error_address = False
        error_qty = False
        item = Item.objects.get(id=item_id)

        if request.method == 'POST':
            order_form = DoOrderForm(request.POST)

            if order_form.is_valid():
                # Ready Info
                user = User.objects.get(django_user=request.user)
                qty = order_form.cleaned_data['qty']
                total_price = order_form.cleaned_data['total_price']
                payment_meth = order_form.cleaned_data['payment_meth']

                # Verifications & Purchase
                if user.address:
                    if item.stock > qty:
                        order = Order(qty, user, item, total_price, ORDER_STATE[0][0], payment_meth)
                        item.stock = item.stock - qty
                        item.save()
                        order.save()
                        return render(request, 'Account.html', {'orders': user.order_set})
                    else:
                        error_qty = True
                else:
                    error_address = True
        else:
            order_form = DoOrderForm(initial={'qty': 1, 'total_price': item.price})

        return render(request, 'DoOrder.html',
                      {'order_form': order_form, 'error_address': error_address, 'error_qty': error_qty})
    else:
        return redirect(request.META['HTTP_REFERER'])  # Redirect to previous url


def add_to_Cart(request, item_id):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        item = Item.objects.get(id=item_id)

        # Load User_Cart
        user_cart = Cart.objects.get(user=user)

        # Save item in Cart
        duplicated_item = Cart_Item.objects.filter(cart=user_cart, item=item)
        if duplicated_item:
            duplicated_item[0].qty = duplicated_item[0].qty + 1
            duplicated_item[0].save()
        else:
            cart_item = Cart_Item(cart=user_cart, item=item, qty=1)
            cart_item.save()

        # Update Total Price
        new_total = 0
        for cart_item in user_cart.cart_item_set.all():
            new_total += cart_item.item.price * cart_item.qty

        user_cart.total_price = new_total
        user_cart.save()

        return redirect(request.META['HTTP_REFERER'])  # redirect to previous url
    else:
        # Maybe later, save cart items in cache when not authenticated?
        return redirect(request.META['HTTP_REFERER'])  # Redirect to previous url


def rem_from_Cart(request, item_id):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_cart = Cart.objects.get(user=user)
        item = Item.objects.get(id=item_id)

        cart_item = Cart_Item.objects.get(cart=user_cart, item=item)
        if cart_item:
            cart_item.delete()
    else:
        # Maybe later, save cart items in cache when not authenticated?
        return redirect(request.META['HTTP_REFERER'])  # Redirect to previous url


def add_to_Wishlist(request, prod_id):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        prod = Product.objects.get(id=prod_id)

        # Load User_Wishlist
        user_wishlist = WishList.objects.get(user=user)

        # Save Product in Cart
        if prod not in user_wishlist.prods.all():
            print("product that will be added:")
            print(prod)
            user_wishlist.prods.add(prod)
        else:
            print("already have this product")

        return redirect(request.META['HTTP_REFERER'])  # redirect to previous url
    else:
        # Maybe later, save cart items in cache when not authenticated?
        return redirect(request.META['HTTP_REFERER'])  # Redirect to previous url


def rem_from_Wishlist(request, prod_id):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        prod = Product.objects.get(id=prod_id)
        user_wishlist = WishList.objects.get(user=user)

        if prod in user_wishlist.prods.all():
            user_wishlist.prods.remove(prod)
        return redirect(request.META['HTTP_REFERER'])  # redirect to previous url
    else:
        # Maybe later, save cart items in cache when not authenticated?
        return redirect(request.META['HTTP_REFERER'])  # Redirect to previous url


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
