from django.http import HttpResponse
from rest_framework import views, pagination
from drf.serializer import ProductInventorySerializer
from search.documents import ProductInventoryDocuments
from elasticsearch_dsl import Q

class SearchProductInventory(views.APIView, pagination.LimitOffsetPagination):
    productinventoryserializer = ProductInventorySerializer
    search_document = ProductInventoryDocuments

    def get(self, request, query):
        try:
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'sku',
                ]
            )
            print(1)
            search = self.search_document.search().query(q)
            print(1)
            response = search.execute()
            print(1)
            results = self.paginate_queryset(response, request, view=self)
            serialize = self.productinventoryserializer(results, many=True)
            return self.get_paginated_response(serialize.data)
        except Exception as e:
            return HttpResponse(e, status=500)
