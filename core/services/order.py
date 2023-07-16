import time
from django.shortcuts import get_object_or_404

from core.decorators import is_authenticated_user, is_user_admin, is_user_staff
from core.enumerations import OrderStatusEnum
from core.serializers.order import OrderResponseSerializer
from ..models import OrderProductMap, OrderStatus, OrderTable, UserOrderMap
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import json


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTable
        fields = "__all__"


class OrderService:

    """
    Since A user can habve only one cart {for now}
    we will create the cart when the cart is created
    This logic should move out when cart is becoming independent
    """

    @api_view(["POST"])
    @is_user_staff
    def create_order(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            order = OrderTable.objects.create(**body)
            current_time_in_epoch = int(time.time())
            order_status = OrderStatus(
                order_id=order.id,
                status=OrderStatusEnum.PLACED.value,
                created_at=current_time_in_epoch,
                updated_at=current_time_in_epoch,
            )
            order_status.save()
            order_products = OrderProductMap.objects.filter(order_id=order.id).all()

            return Response(
                {
                    "status": "success",
                    "message": "Order Placed successfully",
                    "data": OrderResponseSerializer(
                        {
                            "order_details": order,
                            "user_id": self.user.id,
                            "order_status": order_status,
                            "order_products": order_products,
                        }
                    ).data["order_details"],
                },
                status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_user_staff
    def get_order(self, id):
        try:
            order = OrderTable.objects.get(id=id)
            order_status = get_object_or_404(OrderStatus, order_id=order.id)
            order_products = OrderProductMap.objects.filter(order_id=order.id).all()

            return Response(
                {
                    "status": "success",
                    "message": "Order Placed successfully",
                    "data": OrderResponseSerializer(
                        {
                            "order_details": order,
                            "user_id": self.user.id,
                            "order_status": order_status,
                            "order_products": order_products,
                        }
                    ).data["order_details"],
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    @is_user_staff
    def update_order(self, id):
        try:
            body = json.loads(self.body.decode("utf-8"))
            order = OrderTable.objects.get(id=id)
            for key in body:
                setattr(order, key, body[key])
            order.save()
            order_status = get_object_or_404(OrderStatus, order_id=order.id)
            order_products = OrderProductMap.objects.filter(order_id=order.id).all()

            return Response(
                {
                    "status": "success",
                    "message": "Order Placed successfully",
                    "data": OrderResponseSerializer(
                        {
                            "order_details": order,
                            "user_id": self.user.id,
                            "order_status": order_status,
                            "order_products": order_products,
                        }
                    ).data["order_details"],
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["DELETE"])
    @is_user_admin
    def delete_order(self, id):
        """
        Restricted for admin use
        """
        try:
            order = OrderTable.objects.get(id=id)

            order_products = OrderProductMap.objects.filter(order_id=order.id).all()
            for order_product in order_products:
                order_product.delete()

            order_status = OrderStatus.objects.filter(order_id=order.id)
            user_order = UserOrderMap.objects.filter(order_id=order.id)
            user_order.delete()
            order_status.delete()
            order.delete()

            return Response(
                {"status": "success", "message": "Order deleted successfully"},
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_authenticated_user
    def get_all_orders(self):
        try:
            orders = OrderTable.objects.all()

            order_response_list = []
            for order in orders:
                order_status = get_object_or_404(OrderStatus, order_id=order.id)
                order_products = OrderProductMap.objects.filter(order_id=order.id).all()
                order_response_list.append(
                    OrderResponseSerializer(
                        {
                            "order_details": order,
                            "user_id": self.user.id,
                            "order_status": order_status,
                            "order_products": order_products,
                        }
                    ).data["order_details"]
                )

            return Response(
                {"status": "success", "data": order_response_list},
                status.HTTP_200_OK,
            )
        except Exception as e:
            print("Exception::", e)
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_authenticated_user
    def get_all_orders_by_user(self):
        try:
            user_order_id_list = (
                UserOrderMap.objects.filter(user_id=self.user.id)
                .values_list("order_id", flat=True)
                .distinct()
            )
            user_orders_list = OrderTable.objects.filter(id__in=user_order_id_list)
            order_response_list = []
            for order in user_orders_list:
                order_status = get_object_or_404(OrderStatus, order_id=order.id)
                order_products = OrderProductMap.objects.filter(order_id=order.id).all()
                order_response_list.append(
                    OrderResponseSerializer(
                        {
                            "order_details": order,
                            "user_id": self.user.id,
                            "order_status": order_status,
                            "order_products": order_products,
                        }
                    ).data["order_details"]
                )

            return Response(
                {"status": "success", "data": order_response_list},
                status.HTTP_200_OK,
            )
        except Exception as e:
            print("Exception::", e)
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
