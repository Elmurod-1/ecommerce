from django.shortcuts import render
from inventory import models

def home(request):
    return render(request, "demo/index.html")

def category(request):
    data = models.Category.objects.all()
    return render(request, "demo/categories.html", {"data": data})

def product_by_category(request, category):
    data = models.Product.objects.filter(category__name=category).values(
        'id', 'name', 'slug', 'category__name',
        'product__store_price',
        'product__brand__name',
    )
    return render(request, "demo/product_by_category.html", {"data": data})

def product_detail(request, slug):

    filter_argument = []

    if request.GET:
        for value in request.GET.values():
            filter_argument.append(value)

    from django.db.models import Count

    data = models.ProductInventory.objects.filter(product__slug=slug).filter(
        attribute_values__attribut_value__in=filter_argument).annotate(num_tegs=Count('attribute_values')).values(
        'id', 'sku', 'product__name', 'stock_product__units')
    return render(request, "demo/product_detail.html", {"data": data})
