from django.contrib.postgres.aggregates import ArrayAgg
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
        'product__store_price')

    return render(request, "demo/product_by_category.html", {"data": data})


def product_detail(request, slug):
    filter_argument = []
    if request.GET:
        for value in request.GET.values():
            if 'null' != value:
                filter_argument.append(value)

        from django.db.models import Count
        data = models.ProductInventory.objects.filter(product__slug=slug).filter(
            attribute_values__attribute_value__in=filter_argument).annotate(num_tags=Count('attribute_values')). \
            filter(num_tags=len(filter_argument)).values(
            'id', 'sku', 'product__name', 'product__category__name', 'store_price', 'product_inventory__units').get()
    else:
        data = models.ProductInventory.objects.filter(product__slug=slug).filter(is_default=True).values(
            'id', 'sku', 'product__name', 'product__category__name', 'store_price', 'product_inventory__units').annotate(
            field_a=ArrayAgg('attribute_values__attribute_value')).get()
    y = models.ProductInventory.objects.filter(product__slug=slug).distinct().values("attribute_values__product_attribute__name",
                                                                                     "attribute_values__attribute_value")
    z = models.ProductTypeAttribute.objects.filter(product_type__product_type__product__slug=slug).values(
        "product_attribute__name").distinct()

    return render(request, "demo/product_detail.html", {"data": data, 'y': y, 'z': z})
