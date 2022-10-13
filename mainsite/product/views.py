from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators  import action
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product, ProductTag
from .serializers import ProductSerializer
from .permissions import  AuthorAllStaffAllButEditOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset           = Product.objects.all()
    serializer_class   = ProductSerializer
    permission_classes = [AuthorAllStaffAllButEditOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['stock', 'sale_price'] # ?ordering= -> 정렬을 허용할 필드의 화이트 리스트. 미지정 시에 serializer_class에 지정된 필드들.
    ordering        = ['sale_price'] # 디폴트 정렬을 지정
    
    def create(self, request):
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
        product_instance.stock = data.get('stock', product_instance.stock)

        try:
            product_tag = data.get("producttags")
            test_product = ProductTag.objects.get(tagid = data.get('id'))
            test_product.tags = product_tag[0]["tags"]

            test_product.save()
            product_instance.save()
        except:
            pass

        serializer = ProductSerializer(product_instance)
        return Response(serializer.data)
        
