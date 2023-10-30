from django.db import models
from cloudinary.models import CloudinaryField
from django.dispatch import receiver


class CategoryMod(models.Model):
    CATEGORY_CHOICES = (
        ('caps', 'Caps'),
        ('t-shirts', 'T-Shirts'),
        ('pens', 'Pens'),
        ('mugs', 'Mugs'),
        ('bags', 'Bags'),
    )

    name = models.CharField(
        max_length=254, verbose_name='Category Name', choices=CATEGORY_CHOICES)
    friendly_name = models.CharField(
        max_length=254, null=True, blank=True, verbose_name='Friendly Name')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
