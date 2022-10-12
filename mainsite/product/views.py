from rest_framework.response import Response
from rest_framework import viewsets, status

from .models import Product, ProductTag
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None, *args, **kwargs):
        data = request.data

        product_instance = self.get_object()

        product_instance.name            = data.get('name', product_instance.name)
        product_instance.sale_price      = data.get('sale_price', product_instance.sale_price)
        product_instance.price           = data.get('price', product_instance.price)
        product_instance.is_out_of_stock = data.get('is_out_of_stock', product_instance.is_out_of_stock)

        product_tag = data.get("producttags")
        test_product = ProductTag.objects.get(tagid = data.get('id'))
        test_product.tags = product_tag[0]["tags"]

        test_product.save()
        product_instance.save()

        serializer = ProductSerializer(product_instance)
        return Response(serializer.data)
        
