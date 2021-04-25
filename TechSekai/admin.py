from django.contrib import admin
from TechSekai.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Item)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Cart_Item)
admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(Order)

## TODO: JA CRIEI OS MODELOS COM OS SEGUINTES COMANDOS
# para confirmar modelos usar -> python3 manage.py check
# python3 manage.py makemigrations TechSekai
# python3 manage.py sqlmigrate TechSekai 0001 > ./BD_files/db_sql.txt
# python3 manage.py migrate

## TODO: CONTA SUPERUSER CRIADA COM USER:Admin e PASS:ADMIN
# python manage.py createsuperuser

## TODO: NOTA -> PRA DAR RESET À BD, DROP DAS TABELAS E VOLTAR A CRIAR, AQUANDO DE ALTERACOES NOS MODELOS
# 1.python3 manage.py migrate TechSekai zero
# 2.Os 3 comandos de cima novamente
