from xxlimited import Null
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product


# Create your tests here.
class ProductViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_A_manager = User.objects.create(username="상품 A 담당자")
        self.product_B_manager = User.objects.create(username="상품 B 담당자")

    def test_product_create_view(self):
        """
        상품 생성 API 테스트
        """
        self.client.force_login(self.product_A_manager)

        data = {
            "name": "상품 b",
            "manager": self.product_A_manager.id,
            "sale_price": 10000,
            "price": 12000,
            "stock": False,
            "producttags": [{"tags":"aaaa"}]
        }

        res = self.client.post("/product/", data=data, content_type="application/json")

        self.assertEqual(res.status_code, 201)


    def test_product_update_view(self):
        """
        상품 수정 API 테스트
        """
        self.test_product_create_view()  # 상품 A 생성

        product = Product.objects.filter(manager=self.product_A_manager).first()
        self.assertIsNotNone(product)

        self.client.force_login(self.product_A_manager)

        data = {
            "stock": False,
            "producttags": [{"tags":"ccc"}]
            }

        res = self.client.patch(
            f"/product/{product.id}/", data=data, content_type="application/json"
        )

        self.assertEqual(res.status_code, 200)
        # 상품 B 담당자가 상품 A 수정
        self.client.force_login(self.product_B_manager)

        data = {
            "producttags": [{"tags":"test"}]
        }

        res = self.client.patch(
            f"/product/{product.id}/", data=data, content_type="application/json"
        )

        self.assertEqual(res.status_code, 403)

    def test_product_list_view(self):
        """
        상품 리스트 API test
        """
        # 상품 15개 생성
        for _ in range(15):
            self.test_product_create_view()

        self.client.force_login(self.product_A_manager)

        res = self.client.get("/product/")

        self.assertEqual(len(res.json()), 4)

        # 상품 sale_price 내림차순 조회
        self.client.force_login(self.product_A_manager)

        res = self.client.get("/product/?ordering=sale_price")

        self.assertEqual(len(res.json()), 4)


    def test_product_filter_view(self):
        """
        상품 필터 API test
        """

        data = {
            "name": "bal",
            "manager": self.product_A_manager.id,
            "sale_price": 10000,
            "price": 12000,
            "stock": False,
            "producttags": [{"tags":"aaaa"}]
        }
        res = self.client.post("/product/", data=data, content_type="application/json")
        res = self.client.get("/product/?name=bal")
        self.assertEqual(len(res.json()), 1)

        res = self.client.get("/product/?price=12000")
        self.assertEqual(len(res.json()), 1)

        res = self.client.get("/product/?sale_price=10000")
        self.assertEqual(len(res.json()), 1)

    def test_product_search_view(self):
        """
        상품 검색 API test
        """

        data = {
            "name": "bal",
            "manager": self.product_A_manager.id,
            "sale_price": 10000,
            "price": 12000,
            "stock": False,
            "producttags": [{"tags":"aaaa"}]
        }
        res = self.client.post("/product/", data=data, content_type="application/json")
        res = self.client.get("/product/?search=bal")
        self.assertEqual(len(res.json()), 1)

        res = self.client.get("/product/?search=12000")
        self.assertEqual(len(res.json()), 1)

        res = self.client.get("/product/?search=10000")
        self.assertEqual(len(res.json()), 1)

    def test_product_search_view(self):
        """
        상품 검색 API test
        """

        data = {
            "name": "bal",
            "manager": self.product_A_manager.id,
            "sale_price": 10000,
            "price": 12000,
            "stock": False,
            "producttags": [{"tags":"aaaa"}]
        }
        res = self.client.post("/product/", data=data, content_type="application/json")
        res = self.client.get("/product/?search=bal")
        self.assertEqual(len(res.json()), 1)

        res = self.client.get("/product/?search=12000")
        self.assertEqual(len(res.json()), 1)

        res = self.client.get("/product/?search=10000")
        self.assertEqual(len(res.json()), 1)
