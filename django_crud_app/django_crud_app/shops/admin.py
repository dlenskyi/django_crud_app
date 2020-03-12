from django.contrib import admin
from .models import Shop


class ShopAdmin(admin.ModelAdmin):
    model = Shop
    list_display = ['name', 'shop_number', 'owner']
    search_fields = ['name', 'owner']


admin.site.register(Shop, ShopAdmin)
