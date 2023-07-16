from django.shortcuts import get_object_or_404
from core.decorators import is_authenticated_user, is_user_admin, is_user_staff

from core.serializers.product import (
    CategorySerializer,
    ProductCategoryResponseSerializer,
)
from ..models import (
    Category,
    ProductCategoryMap,
    ProductCategoryPriceMap,
    ProductInventoryMap,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


class ProductCategoryService:

    """
    Since A user can habve only one cart {for now}
    we will create the cart when the cart is created
    This logic should move out when cart is becoming independent
    """

    @api_view(["POST"])
    @is_user_staff
    def create_product_category(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product_category = Category.objects.create(**body)

            return Response(
                {
                    "status": "success",
                    "data": CategorySerializer(product_category).data,
                },
                status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_user_staff
    def get_product_category(self, id):
        try:
            product_category = Category.objects.get(id=id)
            return Response(
                {
                    "status": "success",
                    "data": CategorySerializer(product_category).data,
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_user_staff
    def get_all_product_categories(self):
        try:
            product_category_list = Category.objects.all()
            return Response(
                {
                    "status": "success",
                    "data": CategorySerializer(product_category_list, many=True).data,
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            print("Exception::", e)
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    @is_user_staff
    def update_product_category(self, id):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product_category = Category.objects.get(id=id)
            for key in body:
                setattr(product_category, key, body[key])
            product_category.save()

            return Response(
                {
                    "status": "success",
                    "data": CategorySerializer(product_category).data,
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["DELETE"])
    @is_user_admin
    def delete_product_category(self, id):
        """
        Restricted for admin use
        """
        try:
            product_category = Category.objects.get(id=id)
            product_category.delete()

            return Response(
                {
                    "status": "success",
                    "data": CategorySerializer(product_category).data,
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["POST"])
    @is_user_staff
    def add_product_to_category(self):
        try:
            body = json.loads(self.body.decode("utf-8"))

            product_category_response_list = []
            for obj in body:
                product_category = ProductCategoryMap.objects.create(
                    product_id=obj["product_id"], category_id=obj["category_id"]
                )
                category = get_object_or_404(Category, id=obj["category_id"])
                (
                    product_category_price,
                    product_category_price_created,
                ) = ProductCategoryPriceMap.objects.get_or_create(
                    product_category_id=product_category.id
                )
                if product_category_price_created:
                    product_category_price.price = obj["price"]

                quantity = 0
                weight = 0
                if "quantity" in obj:
                    quantity = obj["quantity"]
                if "weight" in obj:
                    weight = obj["weight"]

                product_category_inventory = ProductInventoryMap.objects.get_or_create(
                    product_category_id=product_category.id
                )
                product_category_inventory.quantity = quantity
                product_category_inventory.weight = weight

                product_category_response_list.append(
                    ProductCategoryResponseSerializer(
                        {
                            "category_details": category,
                            "product_category_price_details": product_category_price,
                            "product_inventory_details": product_category_inventory,
                        }
                    ).data["product_category_details"]
                )

            return Response(
                {
                    "status": "success",
                    "data": product_category_response_list,
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    @is_user_staff
    def remove_product_from_category(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            for obj in body:
                for category_id in obj["category_id"]:
                    product_category = get_object_or_404(
                        ProductCategoryMap,
                        product_id=obj["product_id"],
                        category_id=category_id,
                    )
                    product_category_price = get_object_or_404(
                        ProductCategoryPriceMap, product_category_id=product_category.id
                    )
                    product_category_inventory = get_object_or_404(
                        ProductInventoryMap, product_category_id=product_category.id
                    )
                    product_category_inventory.delete()
                    product_category.delete()
                    product_category_price.delete()

            return Response(
                {
                    "status": "success",
                    "message": "Product categories, prices and inventory removed successfully",
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
