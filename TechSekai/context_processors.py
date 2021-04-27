from django.core.cache import cache
from TechSekai.models import *
from TechSekai.templatetags.auth_extras import *


def category_context_processor(request):
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories)

    content = {'all_categories': categories}

    if request.user.is_authenticated and request.user.username != 'Admin' and not has_group(request.user, 'shops'):
        u1 = User.objects.get(django_user=request.user)
        c = Cart.objects.filter(user=u1)
        if c.exists():
            cart = Cart_Item.objects.filter(cart=c[0]).count()
            content.update({'cart': cart})

        if WishList.objects.filter(user=u1).exists():
            w = WishList.objects.get(user=u1)
            wishList = len(w.prods.all())
            content.update({'wishList': wishList})

    return content
