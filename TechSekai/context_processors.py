from django.core.cache import cache

from TechSekai.forms import RegisterDjangoUserForm, LoginDjangoUserForm
from TechSekai.models import *
from TechSekai.templatetags.auth_extras import *


def category_context_processor(request):
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories)

    content = {'all_categories': categories.exclude(name='Other')}

    if request.user.is_authenticated and request.user.username != 'Admin' and not has_group(request.user, 'shops'):
        try:
            u1 = User.objects.get(django_user=request.user)
        except:
            u1 = User(django_user=request.user)
            u1.save()
            cart = Cart(user=u1)
            wishlist = WishList(user=u1)
            cart.save()
            wishlist.save()
        c = Cart.objects.filter(user=u1)
        if c.exists():
            cart = Cart_Item.objects.filter(cart=c[0]).count()
            content.update({'cart': cart})

        if WishList.objects.filter(user=u1).exists():
            w = WishList.objects.get(user=u1)
            wishList = len(w.prods.all())
            content.update({'wishList': wishList})

        viewed = []
        if 'viewed' in request.session:
            for i in request.session['viewed']:
                viewed.append(Product.objects.get(id=i))
            content.update({'viewed': viewed})
    return content
