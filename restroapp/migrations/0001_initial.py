# Generated by Django 5.0.7 on 2024-07-17 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Product Name')),
                ('pdetail', models.CharField(max_length=100, verbose_name='Product Details')),
                ('cat', models.IntegerField(choices=[(1, 'Pizza'), (2, 'Burger'), (3, 'Meal'), (4, 'Cold Drinks')], verbose_name='Catagory')),
                ('price', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
