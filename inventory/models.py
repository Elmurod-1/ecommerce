from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=False, blank=True,
                            verbose_name="category name",
                            help_text="format: required, max-255")
    slug = models.SlugField(max_length=255, null=False, unique=False, blank=False,
                            verbose_name="category safe url",
                            help_text="format:required, letters, numbers, anderscores or hyphens")
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, related_name="children", null=True,
                               blank=True, unique=False, verbose_name="parent of category",
                               help_text="format: not required")

    class Meta:
        verbose_name = "product category"
        verbose_name_plural = "product categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    web_id = models.CharField(max_length=50,
                              unique=True,
                              null=False,
                              blank=False,
                              verbose_name="product website ID",
                              help_text="format:required, unique")
    slug = models.SlugField(max_length=255, null=False, unique=False, blank=False,
                            verbose_name="product safe url",
                            help_text="format:required, letters, numbers, anderscores or hyphens")
    name = models.CharField(max_length=255, null=False, unique=False, blank=True,
                            verbose_name="product name",
                            help_text="format: required, max-255")
    description = models.TextField(null=False, unique=False, blank=True,
                            verbose_name="product description",
                            help_text="format: required")
    category = models.ManyToManyField(Category)
    is_active = models.BooleanField(default=True, verbose_name="product visibility", help_text="format: true=product visible")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="date product created", help_text="format: Y-m-d H:M:S")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="date product updated", help_text="format: Y-m-d H:M:S")

    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True, blank=True,
                            verbose_name="type of product",
                            help_text="format: required,unique, max-255")
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True, blank=True,
                            verbose_name="brand name",
                            help_text="format: required,unique, max-255")

    def __str__(self):
        return self.name

class ProductInventory(models.Model):
    sku = models.CharField(max_length=20,
                           unique=True,
                           null=False,
                           blank=False,
                           verbose_name="stock keeping unit",
                           help_text="format:required, unique, max-20")
    upc = models.CharField(max_length=12,
                           unique=True,
                           null=False,
                           blank=False,
                           verbose_name="universal product code",
                           help_text="format:required, unique, max-12")
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="product_type")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="brand")
    attribute_values = models.ManyToManyField("ProductAttributValue",
                                              related_name="product_attribute_values", through="ProductAttributValues")
    is_active = models.BooleanField(default=True, verbose_name="product visibility",
                                    help_text="format: true=product visible")
    is_default = models.BooleanField(default=False, verbose_name="default ",
                                    help_text="format: true=product visible")
    retail_price = models.DecimalField(max_digits=8,
                                       decimal_places=2,
                                       verbose_name="recommended retail price",
                                       help_text="format: maximum price 999999.99",
                                       error_messages={
                                           "name": {
                                               "max_length": "the price must be between 0 and 999999.99"
                                           }
                                       })
    store_price = models.DecimalField(max_digits=8,
                                      decimal_places=2,
                                      verbose_name="recommended retail price",
                                      help_text="format: maximum price 999999.99",
                                      error_messages={
                                          "name": {
                                              "max_length": "the price must be between 0 and 999999.99"
                                          }
                                      })
    sale_price = models.DecimalField(max_digits=8,
                                     decimal_places=2,
                                     verbose_name="recommended retail price",
                                     help_text="format: maximum price 999999.99",
                                     error_messages={
                                         "name": {
                                             "max_length": "the price must be between 0 and 999999.99"
                                         }
                                     })
    weight = models.FloatField(verbose_name="product weight")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="date sub-product created",
                                      help_text="format: Y-m-d H:M:S")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="date sub-product updated",
                                      help_text="format: Y-m-d H:M:S")

    def __str__(self):
        return self.product.name

class Media(models.Model):
    product_inventory = models.ForeignKey(ProductInventory, on_delete=models.PROTECT, related_name="media_product")
    image = models.ImageField(upload_to='images/', default='images/car.png')
    alt_text = models.CharField(max_length=255,
                           unique=False,
                           null=False,
                           blank=False,
                           verbose_name="alternative text",
                           help_text="format:required, max-255")
    is_feature = models.BooleanField(default=True, verbose_name="product default image",
                                    help_text="format: true=default image")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="date sub-product created",
                                      help_text="format: Y-m-d H:M:S")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="date sub-product updated",
                                      help_text="format: Y-m-d H:M:S")


class Stock(models.Model):
    product_inventory = models.ForeignKey(ProductInventory, on_delete=models.PROTECT, related_name="stock_product")
    last_checked = models.DateTimeField(default=0, null=True, blank=True, verbose_name="inventory stock check date",
                                      help_text="format: Y-m-d H:M:S, null=true, blank=true")
    units = models.IntegerField(default=0, null=False, blank=False, verbose_name="units/qty of stock",
                                      help_text="format: required, default=1")
    units_solid = models.IntegerField(default=0, null=False, blank=False, verbose_name="units/qty of stock",
                                help_text="format: required, default=1")


class ProductAttribut(models.Model):
    name = models.CharField(max_length=255,
                           unique=True,
                           null=False,
                           blank=False,
                           verbose_name="peoduct atribute name",
                           help_text="format:required, unique, max-255")
    description = models.CharField(max_length=255,
                           unique=False,
                           null=False,
                           blank=False,
                           verbose_name="peoduct atribute description",
                           help_text="format:required")

    def __str__(self):
        return self.name

class ProductAttributValue(models.Model):
    product_attribute = models.ForeignKey(ProductAttribut,
                                         related_name="product_atribute", on_delete=models.PROTECT)

    attribut_value = models.CharField(max_length=255,
                           null=False,
                           blank=False,
                           verbose_name="atribute value",
                           help_text="format:required, unique, max-255")

    def __str__(self):
        return f"{self.product_attribute.name}:{self.attribut_value}"

class ProductAttributValues(models.Model):
    attributevalues = models.ForeignKey(ProductAttributValue,
                                         related_name="product_atribute_value", on_delete=models.PROTECT)

    productinventry = models.ForeignKey(ProductInventory,
                                          related_name="product_inventory", on_delete=models.PROTECT)

    class Meta:
        unique_together = (("attributevalues", "productinventry"))


class ProductTypeAtribute(models.Model):
    product_atribute = models.ForeignKey(ProductAttribut, related_name='productatribute', on_delete=models.PROTECT)
    product_type = models.Fo