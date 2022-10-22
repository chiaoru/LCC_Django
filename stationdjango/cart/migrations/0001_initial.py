# Generated by Django 4.1.1 on 2022-09-25 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.IntegerField(default=0)),
                ('shipping', models.IntegerField(default=0)),
                ('grandtotal', models.IntegerField(default=0)),
                ('guestName', models.CharField(max_length=100)),
                ('guestMail', models.CharField(max_length=100)),
                ('guestPhone', models.CharField(max_length=50)),
                ('guestAddress', models.CharField(max_length=200)),
                ('payType', models.CharField(max_length=20)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=100)),
                ('unitprice', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('dtotal', models.IntegerField(default=0)),
                ('detaiOrder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.ordersmodel')),
            ],
        ),
    ]
