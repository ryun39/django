from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Product, ProductTag

class ProductTagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductTag
        fields = ["tags"]

class ProductListSerializer(serializers.ModelSerializer):
    producttags = ProductTagsSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "manager",
            "price",
            "sale_price",
            "stock",
            "producttags",
        ]

class ProductCreateSerializer(serializers.ModelSerializer):
    producttags = ProductTagsSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "manager",
            "price",
            "sale_price",
            "stock",
            "producttags",
        ]

    def create(self, validated_data):
        tag_data = validated_data.pop('producttags')
        id = Product.objects.create(**validated_data)
        for tag in tag_data:
            ProductTag.objects.create(tagid=id, **tag)
        return id

class ProductSerializer(serializers.ModelSerializer):
    producttags = ProductTagsSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "manager",
            "price",
            "sale_price",
            "stock",
            "producttags",
        ]

    def create(self, validated_data):
        tag_data = validated_data.pop('producttags')
        id = Product.objects.create(**validated_data)
        for tag in tag_data:
            ProductTag.objects.create(tagid=id, **tag)
        return id