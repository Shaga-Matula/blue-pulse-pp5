# Generated by Django 3.2.22 on 2023-10-30 11:36

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('caps', 'Caps'), ('t-shirts', 'T-Shirts'), ('pens', 'Pens'), ('mugs', 'Mugs'), ('bags', 'Bags')], max_length=254, verbose_name='Category Name')),
                ('friendly_name', models.CharField(blank=True, max_length=254, null=True, verbose_name='Friendly Name')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='MerchandiseMod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(blank=True, max_length=254, null=True, verbose_name='SKU')),
                ('name', models.CharField(max_length=254, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Price')),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Rating')),
                ('image', cloudinary.models.CloudinaryField(blank=True, default='placeholder', max_length=255, null=True, verbose_name='image')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='merchandise.categorymod', verbose_name='Category')),
            ],
            options={
                'verbose_name_plural': 'Merchandise',
            },
        ),
    ]
