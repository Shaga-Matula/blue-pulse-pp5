from django.db import models
from django.dispatch import receiver


class CategoryMod(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    CATEGORY_CHOICES = (
        ('clothes', 'Clothes'),
        ('memorabilia', 'Memorabilia'),
        ('cd', 'CD'),
    )

    name = models.CharField(max_length=254,
                            verbose_name='Category Name',
                            choices=CATEGORY_CHOICES)
    friendly_name = models.CharField(max_length=254,
                                     null=True,
                                     blank=True, verbose_name='Friendly Name')

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class MerchandiseMod(models.Model):
    category = models.ForeignKey('CategoryMod',
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='Category')
    sku = models.CharField(max_length=254,
                           null=True,
                           blank=True, verbose_name='SKU', editable=False)
    name = models.CharField(max_length=254, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=6,
                                decimal_places=2, verbose_name='Price')
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True, verbose_name='Rating')
    # image = CloudinaryField('image', default="https://res.cloudinary.com/dsqr7dgjt/image/upload/v1700499377/jnepz9qayczlbb0gqvao.png", null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Merchandise'

    def __str__(self):
        return f"{self.name}"


@receiver(models.signals.post_save, sender=MerchandiseMod)
def generate_sku(sender, instance, **kwargs):
    if not instance.sku:
        instance.sku = 'MERCH-00000000' + str(instance.id)
        instance.save()
