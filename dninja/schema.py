from typing import List
from ninja import ModelSchema, Field
from inventory.models import Category, Product, ProductInventory, Brand, Media, ProductType, ProductAttributeValue


class CategorySchema(ModelSchema):
    class Config:
        model = Category
        model_fields = ['name', 'slug']

class ProductSchema(ModelSchema):
    class Config:
        model = Product
        model_fields = ['name', 'web_id']

class BrandSchema(ModelSchema):
    class Config:
        model = Brand
        model_fields = ['name']

class ProducTypeSchema(ModelSchema):
    class Config:
        model =ProductType
        model_fields = ['name', 'product_type_attributes']

class MediaSchema(ModelSchema):
    image: str
    class Config:
        model = Media
        model_fields = ['image', 'alt_text']

class ProductAttributeValueSchema(ModelSchema):
    class Config:
        model = ProductAttributeValue
        model_fields = '__all__'


class ProductInventorySchema(ModelSchema):
    brand: BrandSchema
    media: List[MediaSchema] = Field(alias='media_product_inventory')
    product: ProductSchema
    product_type: ProducTypeSchema
    attributes: List[ProductAttributeValueSchema] = Field(alias='attribute_values')
    class Config:
        model = ProductInventory
        model_fields = ['sku']
