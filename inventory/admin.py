from django.contrib import admin
from .models import Category, Product, Brand, ProductType, ProductInventory, Media

admin.site.register([Category, Product, Brand, ProductType, ProductInventory, Media])
