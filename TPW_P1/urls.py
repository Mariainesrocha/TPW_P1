from django.contrib import admin
from django.urls import path
from TechSekai import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # GENERAL PAGES
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('hot_deals/', views.hot_deals, name='hot_deals'),
    path('new_arrivals/', views.new_arrivals, name='new_arrivals'),


    # ACCOUNT RELATED
    #path('register', views.register, name='register'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('account/', views.account_page, name='account'),

    # PRODUCT RELATED
    path('product/<int:prod_id>', views.product_shops, name='product_shops'),
    path('do_order/<int:item_id>', views.order_product, name='order_product'),
    path('add_to_cart/<int:item_id>', views.add_to_Cart, name='add_to_cart'),
    path('add_to_wishlist/<int:item_id>', views.add_to_Wishlist, name='add_to_wishlist'),

    ##TODO: NOTA ->  POSSIVEIS URLS + VIEWS NECESSARIAS PRA LOJAS GERIREM SEUS PRODUTOCS
    path('products/add', views.add_product, name='add_product'),
    path('products/', views.list_products, name='products'),
    # path('products/<int:id>', views.see_product, name='see_product'),
    # path('products/edit/<int:id>', views.edit_product, name='edit_product'),
    # path('products/delete/<int:id>', views.delete_product, name='delete_product'),

    ##TODO: NOTA ->  POSSIVEIS URLS + VIEWS NECESSARIAS PRA CONTA
    # path('sign_up/', views.create_account, name='create_account'),
    # path('account/edit/', views.edit_account, name='edit_account'),
    # path('account/add/address/', views.add_address, name='add_address'),
    # path('account/edit/address/', views.edit_address, name='edit_address'),
    # TODO: Encontrei isto pra permitir mudanca de pass c os mecanismos do django como pra login e logout: https://docs.djangoproject.com/en/3.1/topics/auth/default/  -> ver em: Authentication Views¶
    # path('account/change_password/', auth_views.PasswordChangeView.as_view(template_name='change_pwd.html', success_url='/account/password_changed'), name='change_password'),
    # path('account/password_changed', views.password_changed, name='password_changed'),


    ##TODO: NOTA ->  POSSIVEIS URLS + VIEWS NECESSARIAS PRA GESTAO DAS LOJAS
    # path('shops/add', views.add_shop, name='add_shop'),
    # path('shops/', views.list_shops, name='list_shops'),
    # path('shops/<int:id>', views.see_shop, name='see_shop'),
    # path('shops/edit/<int:id>', views.edit_shop, name='edit_shop'),
    # path('shops/delete/<int:id>', views.delete_shop, name='delete_shop'),

    ##TODO: NOTA ->  POSSIVEIS URLS + VIEWS NECESSARIAS PRA CLIENTE FAZER COMPRAS
    # path('account/order/', views.order, name='order'),
    path('account/shoppingcart/', views.cart, name='cart'),
    path('account/checkout/', views.checkout, name='checkout'),
    path('account/wishlist', views.wishlist, name='wishlist'),

    # path('add/<str:pType>/', views.addProduct, name='addProduct'),
    # path('edit/<int:pID>/', views.editProduct, name='editProduct'),
]

## TODO: !!!!!!!!!!!!! IDEIA INTERESSANTE SERIA USAR AS SESSION COOKIES DO DJANGO N SO PRA PESQUISAS, MAS PRA GUARDAR OS PRODUTOS VISTOS RECENTEMENTE, NAO ADICIONADOS AO CARRINHO
