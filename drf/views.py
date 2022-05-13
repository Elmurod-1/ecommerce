from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.response import Response
from inventory import models
from drf import serializer

class AllProductsViewSet( viewsets.GenericViewSet,
                    mixins.ListModelMixin,          # hamma malumotni olish
                    mixins.RetrieveModelMixin,
                    ):
    queryset = models.Product.objects.all()
    serializer_class = serializer.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        if 'slug' in kwargs:
            queryset = models.Product.objects.filter(category__slug=kwargs['slug'])
            serializers = serializer.ProductSerializer(queryset, many=True)
            return Response(serializers.data)
        return self.list(request, *args, **kwargs)             # bu list hamma argumentni qaytaradi

class ProductInventoryVievSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin):
    queryset = models.ProductInventory.objects.all()[:10]
    serializer_class = serializer.ProductInventorySerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        queryset = models.ProductInventory.objects.filter(
            product__category__slug=kwargs['slug']).filter(is_default=True)[:10]
        serializers = serializer.ProductInventorySerializer(queryset, context={'request': request}, many=True)
        return Response(serializers.data)
