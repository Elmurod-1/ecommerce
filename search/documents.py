from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from inventory.models import ProductInventory

@registry.register_document
class ProductInventoryDocuments(Document):
    class Index:
        name = 'productinventory'

    class Django:
        model = ProductInventory

        fields = [
            'id',
            'sku',
            'store_price',
            'is_default',
        ]