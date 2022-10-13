from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    manager = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="상품 담당자")
    name = models.CharField(
        verbose_name= "상품이름",
        max_length=100
    )
    price = models.PositiveIntegerField(
        verbose_name="상품 정가",
    )
    sale_price = models.PositiveIntegerField(
        verbose_name="상품 할인가",
    )
    stock = models.BooleanField(
        verbose_name="제고유무",
        default=True
    )
    class Meta:
        verbose_name = "상품"
        verbose_name_plural="상품"

    def __str__(self):
        return self.name

class ProductTag(models.Model):
    tagid = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="producttags",
    )
    tags = models.CharField(
        verbose_name="상품 태그",
        max_length=100,
        blank=True,
    )
