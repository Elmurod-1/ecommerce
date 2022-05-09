import pytest
from django.db import IntegrityError

from inventory import models

@pytest.mark.dbfixture
@pytest.mark.parametrize("id, name, slug, is_active",
                         [
                             (1, "django", "django", True),         # bu malumotlar db ga kiritilga bo'lsa to'g'ri ishlaydi
                             (2, "django admin", "django-admin", True)        # misol bu db ga kiritilmagan hatolik beradi
                         ],)
def test_inventory_category_dbfixture(db, django_db_setup, id, name, slug, is_active):
    result = models.Category.objects.get(id=id)
    assert result.name == name
    assert result.slug == slug
    assert result.is_active == is_active

@pytest.mark.parametrize("name, slug, is_active",
                         [
                             ("fashion", "fashion", 1),
                             ("trainers", "trainers", 0),
                             ("bascketball", "bascketball", 0),
                         ])
def test_inventory_category_insert_data(db, category_factory, name, slug, is_active):
    result = category_factory.create(name=name, slug=slug, is_active=is_active)
    assert result.name == name
    assert result.slug == slug
    assert result.is_active == is_active


@pytest.mark.dbfixture
@pytest.mark.parametrize("id, web_id, slug, name, description, is_active, created_at, updated_at",
                         [
                            (
        1,
        "456789123",
        "django",
        "django models",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Corporis, quibusdam.",
        True,
        "2022-05-05 07:00:52",
        "2022-05-05 07:00:52",
        ),
        (
        2,
        "123456987",
        "django-admin",
        "django admin model",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Corporis, quibusdam.",
        True,
        "2022-05-05 07:01:23",
        "2022-05-05 07:01:45",
        )
                         ],)
def test_inventory_product_dbfixture(db, django_db_setup, id, web_id, slug, name, description, is_active, created_at, updated_at):
    result = models.Product.objects.get(id=id)
    result_created_at = result.created_at.strftime("%Y-%m-%d %H:%M:%S")
    result_updated_at = result.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    assert result.web_id == web_id
    assert result.name == name
    assert result.slug == slug
    assert result.description == description
    assert result.is_active == is_active
    assert result_created_at == created_at
    assert result_updated_at == updated_at

def test_inventory_db_product_uniqueness_integrity(db, product_factory):
    new_web_id = product_factory.create(web_id=123456789)
    with pytest.raises(IntegrityError):
        product_factory.create(web_id=123456789)

@pytest.mark.dbfixture
def test_inventory_db_product_isert_data(
        db, product_factory, category_factory
):
    new_category = category_factory.create()
    new_product = product_factory.create(category=(1, 2))
    result_product_ctegory = new_product.category.all().count()
    assert "web_id_2" == new_product.web_id
    assert result_product_ctegory == 2


@pytest.mark.dbfixture
@pytest.mark.parametrize("id, sku, upc, product_type, product, brand, is_active, retail_price, store_price, sale_price, weight, created_at, updated_at",
                         [
    (   1,
        "lesson1",
        "123456789",
        1,
        1,
        1,
        True,
        "98.99",
        "100.00",
        "25.00",
        10.0,
        "2022-05-05 12:47:49",
        "2022-05-05 12:47:49"
                         ),
    (   2,
        "lesson2",
        "123654789",
        2,
        2,
        1,
        True,
        "56.00",
        "60.00",
        "19.00",
        7.0,
        "2022-05-05 12:49:03",
        "2022-05-05 12:49:03"
                         )])
def test_inventory_db_product_inventory_dataset(db, django_db_setup,
                                                id, sku, upc, product_type, product, brand, is_active, retail_price, store_price, sale_price, weight, created_at, updated_at):
    result = models.ProductInventory.objects.get(id=id)
    result_created_at = result.created_at.strftime("%Y-%m-%d %H:%M:%S")
    result_updated_at = result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    assert result.sku == sku
    assert result.upc == upc
    assert result.product_type.id == product_type
    assert result.product.id == product
    assert result.brand.id == brand
    assert result.is_active == is_active
    assert result.retail_price.__str__() == retail_price
    assert result.store_price.__str__() == store_price
    assert result.sale_price.__str__() == sale_price
    assert result.weight == weight
    assert result_created_at == created_at
    assert result_updated_at == updated_at

@pytest.mark.dbfixture
def test_inventory_db_product_inventory_insert_data(
        db, product_inventory_factory
):
    new_product = product_inventory_factory.create(
        sku="123456879",
        upc="123457689",
        product_type__name="new_name",
        product__web_id="123456789",
        brand__name="new_name"
    )

    assert new_product.sku == "123456879"
    assert new_product.upc == "123457689"
    assert new_product.product_type.name == "new_name"
    assert new_product.product.web_id == "123456789"
    assert new_product.brand.name == "new_name"
    assert new_product.is_active == 1
    assert new_product.retail_price == 97.00
    assert new_product.store_price == 92.00
    assert new_product.sale_price == 46.00
    assert new_product.weight == 987

def test_inventory_db_producttype_insert_data(db, product_type_factory):
    new_type = product_type_factory.create(name="demo_name")
    assert new_type.name == "demo_name"

def test_inventory_db_producttype_uniqueness_integrity(db, product_type_factory):
    new_type = product_type_factory.create(name="not_unique")
    with pytest.raises(IntegrityError):
        product_type_factory.create(name="not_unique")

def test_inventory_db_brand_insert_data(db, brand_factory):
    new_brand = brand_factory.create(name="demo_name")
    assert new_brand.name == "demo_name"

def test_inventory_db_brand_uniqueness_integrity(db, brand_factory):
    new_brand = brand_factory.create(name="not_unique")
    with pytest.raises(IntegrityError):
        brand_factory.create(name="not_unique")

@pytest.mark.dbfixture
@pytest.mark.parametrize("id, product_inventory, image, alt_text, is_feature, created_at, updated_at",
                         [(
        1,
        1,
        "images/Watch.jpeg",
        "Watch django program",
        True,
        "2022-05-05 15:20:50",
        "2022-05-05 15:20:50"
                         ),
    (   2,
        2,
        "images/T-Shirt.jpeg",
        "T-shirt django admin model",
        True,
        "2022-05-05 15:22:26",
        "2022-05-05 15:22:26"
                         )])
def test_inventory_db_media_dataset(db, django_db_setup, id, product_inventory, image, alt_text, is_feature, created_at, updated_at):
    result = models.Media.objects.get(id=id)
    result_created_at = result.created_at.strftime("%Y-%m-%d %H:%M:%S")
    result_updated_at = result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    assert result.product_inventory.id == product_inventory
    assert result.image == image
    assert result.alt_text == alt_text
    assert result.is_feature == is_feature
    assert result_created_at == created_at
    assert result_updated_at == updated_at

def test_inventory_db_media_insert_data(db, media_factory):
    new_brand = media_factory.create( product_inventory__sku="321456988")
    assert new_brand.product_inventory.sku == "321456988"
    assert new_brand.image.__str__() == "images/cap.png"
    assert new_brand.alt_text == "a default image solid color"
    assert new_brand.is_feature == 1

@pytest.mark.dbfixture
@pytest.mark.parametrize("id, product_inventory, last_checked, units, units_sold",
                         [

                         ])
def test_inventory_db_stock_datase(db, django_db_setup, id, product_inventory, last_checked, units, units_sold):
    result = models.Stock.objects.get(id=id)
    result_last_checked = result.last_checked.strftime("%Y-%m-%d %H:%M:%S")
    assert result.product_inventory.id == product_inventory
    assert result.last_checked == result_last_checked
    assert result.units == units
    assert result.units_sold == units_sold

def test_inventory_db_media_insert_data(db, stock_factory):
    new_stock = stock_factory.create(product_inventory__sku="321456988")
    assert new_stock.product_inventory.sku == "321456988"
    assert new_stock.units == 2
    assert new_stock.units_solid == 100

