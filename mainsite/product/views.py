from .models      import Product, ProductTag
from .serializers import ProductSerializer
from .permissions import AuthorAllStaffAllButEditOrReadOnly

from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend

class ProductPagination(LimitOffsetPagination):
    default_limit = 4

class ProductViewSet(viewsets.ModelViewSet):
    queryset           = Product.objects.all()
    serializer_class   = ProductSerializer

    pagination_class = ProductPagination

    permission_classes = [AuthorAllStaffAllButEditOrReadOnly]
    filter_backends    = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    filterset_fields   = ['name', 'price', 'sale_price', 'stock']
    search_fields      = ['price']
    ordering_fields    = ['price', 'sale_price']
    # Default Ordering
    ordering           = ['sale_price'] # 디폴트 정렬을 지정
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None, *args, **kwargs):
        data = request.data

        product_instance = self.get_object()

        product_instance.name       = data.get('name', product_instance.name)
        product_instance.sale_price = data.get('sale_price', product_instance.sale_price)
        product_instance.price      = data.get('price', product_instance.price)
        product_instance.stock      = data.get('stock', product_instance.stock)

        product_instance.save()

        try:
            request_tag  = data.get("producttags")
            product_tag = ProductTag.objects.get(tagid = data.get('id'))
            product_tag.tags = request_tag[0]["tags"]

            product_tag.save()
        except:
            pass

        serializer = ProductSerializer(product_instance)
        return Response(serializer.data)
        
