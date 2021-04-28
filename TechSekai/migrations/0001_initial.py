# Generated by Django 3.1.2 on 2021-04-28 20:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=10)),
                ('street', models.CharField(max_length=100)),
                ('door', models.IntegerField()),
                ('floor', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('totDevices', models.IntegerField()),
                ('image', models.ImageField(default='images/logo.png', null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('stock', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.PositiveBigIntegerField()),
                ('name', models.CharField(max_length=50)),
                ('details', models.TextField(max_length=300)),
                ('warehouse', models.CharField(max_length=50)),
                ('qty_sold', models.IntegerField()),
                ('image', models.ImageField(blank=True, default='logo.png', null=True, upload_to='images/')),
                ('lowest_price', models.IntegerField(default=100)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.category')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other/Not specified')], max_length=20, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('phone_number', models.PositiveBigIntegerField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TechSekai.address')),
                ('django_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prods', models.ManyToManyField(to='TechSekai.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.user')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('phone_number', models.PositiveBigIntegerField(null=True)),
                ('website', models.URLField(max_length=40, null=True)),
                ('opening_hours', models.TimeField(null=True)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TechSekai.address')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='TechSekai.shop'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('total_price', models.PositiveIntegerField()),
                ('order_state', models.CharField(choices=[('ORDERED', 'Processing order'), ('DISPATCHED', 'Sent to delivery'), ('IN TRANSIT', 'On the way'), ('DELIVERED', 'Delivered at the destination address'), ('REFUND', 'Pay back to a non satisfied client'), ('FAILED', 'Error with the destination address, must contact us')], max_length=20)),
                ('payment_meth', models.CharField(choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal'), ('ATM ', 'ATM'), ('VISA', 'VISA'), ('ApplePay', 'ApplePay')], max_length=20)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.user')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.product'),
        ),
        migrations.AddField(
            model_name='item',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.shop'),
        ),
        migrations.CreateModel(
            name='Cart_Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.item')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TechSekai.user'),
        ),
    ]
