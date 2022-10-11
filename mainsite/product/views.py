from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Product, ProductTag
from .serializers import ProductListSerializer, ProductCreateSerializer, ProductSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer