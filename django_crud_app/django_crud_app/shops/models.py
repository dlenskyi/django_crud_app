from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Shop(models.Model):
    shop_number = models.IntegerField(unique=True, blank=True, null=True)

    name = models.CharField(blank=True, null=True, unique=True, max_length=128)

    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='shop_key_to_user')

    class Meta:
        db_table = 'shop'
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    def __str__(self):
        return f'{self.name} {self.shop_number}'

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Shop.
        """
        return reverse('shop-detail', args=[str(self.id)])
