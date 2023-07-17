import json

from django.shortcuts import get_object_or_404
from core.decorators import is_authenticated_user, is_user_admin
from core.serializers.product import (
    ProductResponseSerializer,
)

from core.serializers.product import (
    ProductCategoryResponseSerializer,
)
from ..models import (
    Category,
    Product,
    ProductCategoryMap,
    ProductCategoryPriceMap,
    ProductInventoryMap,
)
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer


class ProductService:

    """
    Service for following operations related to Product:
    - all CRUD operations
    """

    def _get_product_category_response_details(id):
        product_category_query_set = ProductCategoryMap.objects.filter(product_id=id)

        if not product_category_query_set.exists():
            raise Exception("Product-Category data not found")
        product_category_list = product_category_query_set

        product_category_response_list = []
        for product_category in product_category_list:
            category = get_object_or_404(Category, id=product_category.category_id)
            product_category_price = get_object_or_404(
                ProductCategoryPriceMap, product_category_id=product_category.id
            )
            product_category_inventory = get_object_or_404(
                ProductInventoryMap, product_category_id=product_category.id
            )
            product_category_response_list.append(
                ProductCategoryResponseSerializer(
                    {
                        "category_details": category,
                        "product_category_price_details": product_category_price,
                        "product_inventory_details": product_category_inventory,
                    }
                ).data["product_category_details"]
            )
        return product_category_response_list

    def _create_product_category_details(product_id, req_body):
        product_category_response_list = []
        for obj in req_body["category_price_list"]:
            category = get_object_or_404(Category, id=obj["category_id"])
            product_category = ProductCategoryMap.objects.create(
                product_id=product_id, category_id=obj["category_id"]
            )
            product_category_price = ProductCategoryPriceMap.objects.create(
                product_category_id=product_category.id, price=obj["price"]
            )

            quantity = 0
            weight = 0
            if "quantity" in req_body:
                quantity = obj["quantity"]
            if "weight" in req_body:
                weight = obj["weight"]

            product_category_inventory = ProductInventoryMap.objects.create(
                product_category_id=product_category.id,
                quantity=quantity,
                weight=weight,
            )
            product_category_response_list.append(
                ProductCategoryResponseSerializer(
                    {
                        "category_details": category,
                        "product_category_price_details": product_category_price,
                        "product_inventory_details": product_category_inventory,
                    }
                ).data["product_category_details"]
            )

        return product_category_response_list

    @api_view(["POST"])
    @is_authenticated_user
    def create_product(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product = Product.objects.create(name=body["name"])
            product_category_response_list = (
                ProductService._create_product_category_details(product.id, body)
            )

            return Response(
                {
                    "status": "success",
                    "data": ProductResponseSerializer(
                        {
                            "product_details": product,
                            "category_details": product_category_response_list,
                        }
                    ).data["product_details"],
                },
                status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_authenticated_user
    def get_product(self, id):
        try:
            product = Product.objects.get(id=id)
            product_category_response_list = (
                ProductService._get_product_category_response_details(id)
            )

            return Response(
                {
                    "status": "success",
                    "data": ProductResponseSerializer(
                        {
                            "product_details": product,
                            "category_details": product_category_response_list,
                        }
                    ).data["product_details"],
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    @is_authenticated_user
    def update_product(self, id):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product = Product.objects.get(id=id)
            for key in body:
                setattr(product, key, body[key])
            product.save()

            product_category_response_list = (
                ProductService._get_product_category_response_details(id)
            )

            return Response(
                {
                    "status": "success",
                    "data": ProductResponseSerializer(
                        {
                            "product_details": product,
                            "category_details": product_category_response_list,
                        }
                    ).data["product_details"],
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["DELETE"])
    @is_user_admin
    def delete_product(self, id):
        """
        Restricted for admin use
        """
        try:
            product = Product.objects.get(id=id)

            product_category_query_set = ProductCategoryMap.objects.filter(
                product_id=id
            )
            if not product_category_query_set.exists():
                raise Exception("Product-Category data not found")
            product_category_list = product_category_query_set

            for product_category in product_category_list:
                product_category_price = get_object_or_404(
                    ProductCategoryPriceMap, product_category_id=product_category.id
                )
                product_category_inventory = get_object_or_404(
                    ProductInventoryMap, product_category_id=product_category.id
                )
                product_category_price.delete()
                product_category_inventory.delete()
                product_category.delete()

            product.delete()

            return Response(
                {
                    "status": "success",
                    "message": "Product and category details deleted",
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @renderer_classes([TemplateHTMLRenderer])
    def get_all_products(self):
        try:
            products = Product.objects.all()
            response_list = []
            for product in products:
                product_category_response_list = (
                    ProductService._get_product_category_response_details(product.id)
                )
                response_list.append(
                    ProductResponseSerializer(
                        {
                            "product_details": product,
                            "category_details": product_category_response_list,
                        }
                    ).data["product_details"]
                )

            return Response(
                {
                    "status": "success",
                    "data": response_list,
                },
                template_name="home.html",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("Exception::", e)
            return Response(
                {"status": "failure"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
