from django.shortcuts import get_object_or_404
from core.decorators import is_authenticated_user, is_user_admin

from core.serializers.product import CategorySerializer, ProductInventorySerializer
from ..models import (
    ProductCategoryMap,
    ProductInventoryMap,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


class ProductInventoryService:

    """ "
    ProductInventoryService Service provides the following functionalities:
    - all CRUD operations related to product-inventory
    """

    @api_view(["POST"])
    @is_authenticated_user
    def create_product_category_inventory(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product_category = get_object_or_404(
                ProductCategoryMap,
                product_id=body["product_id"],
                category_id=body["category_id"],
            )
            product_category_inventory = ProductInventoryMap.objects.create(
                product_category_id=product_category.id,
                quantity=body["quantity"],
                weight=body["weight"],
            )

            return Response(
                {
                    "status": "success",
                    "data": ProductInventorySerializer(product_category_inventory).data,
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
    def get_product_category_inventory_by_id(self, id):
        try:
            product_category_inventory = ProductInventoryMap.objects.get(id=id)

            return Response(
                {
                    "status": "success",
                    "data": ProductInventorySerializer(product_category_inventory).data,
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_authenticated_user
    def get_product_category_inventory_by_product(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product_category = get_object_or_404(
                ProductCategoryMap,
                product_id=body["product_id"],
                category_id=body["category_id"],
            )
            product_category_inventory = get_object_or_404(
                ProductInventoryMap, product_category_id=product_category.id
            )

            return Response(
                {
                    "status": "success",
                    "data": ProductInventorySerializer(product_category_inventory).data,
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_authenticated_user
    def get_all_product_category_inventory(self):
        try:
            product_category_inventory_list = ProductInventoryMap.objects.all()
            return Response(
                {
                    "status": "success",
                    "data": ProductInventorySerializer(
                        product_category_inventory_list, many=True
                    ).data,
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            print("Exception::", e)
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    @is_authenticated_user
    def update_product_category_inventory(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product_category = get_object_or_404(
                ProductCategoryMap,
                product_id=body["product_id"],
                category_id=body["category_id"],
            )
            product_category_inventory = get_object_or_404(
                ProductInventoryMap, product_category_id=product_category.id
            )

            product_category_inventory.quantity = body["quantity"]
            product_category_inventory.weight = body["weight"]
            product_category_inventory.save()

            return Response(
                {
                    "status": "success",
                    "data": ProductInventorySerializer(product_category_inventory).data,
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["DELETE"])
    @is_user_admin
    def delete_product_category_inventory(self, id):
        """
        Restricted for admin use
        """
        try:
            body = json.loads(self.body.decode("utf-8"))
            product_category = get_object_or_404(
                ProductCategoryMap,
                product_id=body["product_id"],
                category_id=body["category_id"],
            )
            product_category_inventory = get_object_or_404(
                ProductInventoryMap, product_category_id=product_category.id
            )
            product_category_inventory.delete()

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
