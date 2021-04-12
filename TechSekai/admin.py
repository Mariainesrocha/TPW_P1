from django.contrib import admin
from TechSekai.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Item)


# NECESSARIO???
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(Order)


## TODO: MIGRAR OS MODELOS
# para confirmar modelos usar -> python manage.py check
# python manage.py makemigrations TechSekai
# python manage.py migrate

## TODO 2: CRIAR CONTA ADMIN, PASS:ADMIN
#python manage.py createsuperuser