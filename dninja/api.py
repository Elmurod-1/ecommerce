from typing import List
from ninja import NinjaAPI
from inventory.models import Category, Product, ProductInventory
from .schema import CategorySchema, ProductSchema, ProductInventorySchema


api = NinjaAPI()

@api.get('/inventory/category/all/', response=List[CategorySchema])
def category_list(request):
    qs = Category.objects.all()
    return qs

@api.get('/inventory/product/category/{category_slug}/', response=List[ProductSchema])
def category_list(request, category_slug):
    qs = Product.objects.filter(category__slug=category_slug)
    return qs

@api.get('/inventory/productinventory/', response=List[ProductInventorySchema])
def category_list(request):
    qs = ProductInventory.objects.all()[:10]
    return qs
