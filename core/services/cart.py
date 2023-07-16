import decimal
import time
from django.shortcuts import get_object_or_404
from core import constants
from core.decorators import is_authenticated_user, is_user_admin, is_user_staff
from core.enumerations import OrderStatusEnum
from core.serializers.cart import (
    CartPriceSerializer,
    CartProductSerializer,
    CartResponseSerializer,
    CartSerializer,
    CartUserSerializer,
)

from core.serializers.order import OrderProductSerializer, OrderResponseSerializer
from ..models import (
    Cart,
    CartPriceMap,
    CartProductMap,
    CartUserMap,
    ProductCategoryMap,
    UserOrderMap,
    OrderTable,
    OrderStatus,
    OrderProductMap,
    ProductCategoryPriceMap,
    ProductInventoryMap,
    User,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import json


class CartService:

    """
    Since A user can habve only one cart {for now}
    we will create the cart when the cart is created
    This logic should move out when cart is becoming independent
    """

    def create_new_cart_object(cart_json_obj):
        cart = Cart.objects.create(**cart_json_obj)
        cart_price = CartPriceMap.objects.create(
            cart_id=cart.id,
            total_price=0.0,
            net_total_price=0.0,
            vat_percent=0.0,
            vat_tax_price=0.0,
        )
        print("cart-price-map")
        return cart, cart_price

    @api_view(["POST"])
    @is_user_staff
    def create_cart(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            cart, cart_price = CartService.create_new_cart_object(body)
            cart_products = []

            return Response(
                {
                    "status": "success",
                    "data": CartResponseSerializer(
                        {
                            "cart_details": cart,
                            "user_id": self.user.id,
                            "cart_price_details": cart_price,
                            "cart_products": cart_products,
                        }
                    ).data["cart_details"],
                },
                status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_user_staff
    def get_cart(self, id):
        try:
            cart = Cart.objects.get(id=id)
            cart_price = get_object_or_404(CartPriceMap, cart_id=cart.id)
            cart_products = CartPriceMap.objects.filter(cart_id=cart.id).all()

            return Response(
                {
                    "status": "success",
                    "data": CartResponseSerializer(
                        {
                            "cart_details": cart,
                            "user_id": self.user.id,
                            "cart_price_details": cart_price,
                            "cart_products": cart_products,
                        }
                    ).data["cart_details"],
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    @is_user_staff
    def update_cart(self, id):
        try:
            body = json.loads(self.body.decode("utf-8"))
            cart = Cart.objects.get(id=id)
            for key in body:
                setattr(cart, key, body[key])
            cart.save()
            cart_price = get_object_or_404(CartPriceMap, cart_id=cart.id)
            cart_products = CartPriceMap.objects.filter(cart_id=cart.id).all()

            return Response(
                {
                    "status": "success",
                    "data": CartResponseSerializer(
                        {
                            "cart_details": cart,
                            "user_id": self.user.id,
                            "cart_price_details": cart_price,
                            "cart_products": cart_products,
                        }
                    ).data["cart_details"],
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["DELETE"])
    @is_user_admin
    def delete_cart(self, id):
        """
        Restricted for admin use
        """
        try:
            cart = Cart.objects.get(id=id)
            cart_price = get_object_or_404(CartPriceMap, cart_id=cart.id)
            cart_products = CartPriceMap.objects.filter(cart_id=cart.id).all()
            for cart_product in cart_products:
                cart_product.delete()

            cart_price.delete()
            cart.delete()

            return Response(
                {"status": "success", "message": "Cart details deleted successfully"},
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    @is_authenticated_user
    def clear_cart(self):
        try:
            user_query_set = User.objects.filter(id=self.user.id)
            if not user_query_set.exists():
                raise Exception("User data not found")
            user = user_query_set[0]

            cart_user_query_set = CartUserMap.objects.filter(user_id=user.id)
            if not cart_user_query_set.exists():
                raise Exception("Cart-User-Map data not found")
            cart_user = cart_user_query_set[0]

            cart_product_query_set = CartProductMap.objects.filter(
                cart_id=cart_user.cart_id
            )
            if not cart_product_query_set.exists():
                return Response(
                    {"status": "success", "message": "Cart is empty"},
                    status.HTTP_200_OK,
                )

            cart_product_list = cart_product_query_set
            cart_price = get_object_or_404(CartPriceMap, cart_id=cart_user.cart_id)
            cart = get_object_or_404(Cart, id=cart_user.cart_id)

            for product in cart_product_list:
                product.delete()
            cart_product_list = []

            reset_zero = decimal.Decimal(0.0)
            cart_price.total_price = reset_zero
            cart_price.net_total_price = reset_zero
            cart_price.vat_percent = reset_zero
            cart_price.vat_tax_price = reset_zero
            cart_price.save()

            current_time_in_epoch = int(time.time())
            cart.updated_at = current_time_in_epoch
            cart.save()

            return Response(
                {
                    "status": "success",
                    "data": CartResponseSerializer(
                        {
                            "cart_details": cart,
                            "user_id": self.user.id,
                            "cart_price_details": cart_price,
                            "cart_products": cart_product_list,
                        }
                    ).data["cart_details"],
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_authenticated_user
    def get_all_products_in_cart(self):
        try:
            cart_user_query_set = CartUserMap.objects.filter(user_id=self.user.id)
            if not cart_user_query_set.exists():
                raise Exception("Cart-User-Map data not found")
            cart_user = cart_user_query_set[0]

            cart_product_query_set = CartProductMap.objects.filter(
                cart_id=cart_user.cart_id
            )
            if not cart_product_query_set.exists():
                return Response(
                    {"status": "success", "message": "Cart is empty"},
                    status.HTTP_200_OK,
                )
            cart_products = cart_product_query_set.all()
            cart = get_object_or_404(Cart, id=cart_user.cart_id)
            cart_price = get_object_or_404(CartPriceMap, cart_id=cart.id)

            return Response(
                {
                    "status": "success",
                    "data": CartResponseSerializer(
                        {
                            "cart_details": cart,
                            "user_id": self.user.id,
                            "cart_price_details": cart_price,
                            "cart_products": cart_products,
                        }
                    ).data["cart_details"],
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["POST"])
    @is_authenticated_user
    def add_product_to_cart(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product_category = get_object_or_404(
                ProductCategoryMap,
                product_id=body["product_id"],
                category_id=body["category_id"],
            )

            cart_user_query_set = CartUserMap.objects.filter(user_id=self.user.id)
            if not cart_user_query_set.exists():
                raise Exception("Cart-User-Map data not found")
            cart_user = cart_user_query_set[0]

            product_category_price = get_object_or_404(
                ProductCategoryPriceMap, product_category_id=product_category.id
            )
            product_category_inventory = get_object_or_404(
                ProductInventoryMap, product_category_id=product_category.id
            )

            if body["quantity"] > product_category_inventory.quantity:
                return Response(
                    {"status": "success", "message": "Product out of stock"},
                    status=status.HTTP_202_ACCEPTED,
                )

            cart_product, created = CartProductMap.objects.get_or_create(
                product_id=product_category.product_id,
                category_id=product_category.category_id,
                cart_id=cart_user.cart_id,
            )
            if not created:
                cart_product.quantity += body["quantity"]
            else:
                cart_product.quantity = body["quantity"]

            product_category_inventory.quantity -= body["quantity"]
            cart_product.save()
            product_category_inventory.save()

            current_time_in_epoch = int(time.time())
            cart = Cart.objects.get(id=cart_user.cart_id)
            cart.updated_at = current_time_in_epoch
            cart.save()

            print("cart_user.cart_id ", cart_user.cart_id)
            cart_price = get_object_or_404(CartPriceMap, cart_id=cart_user.cart_id)
            cart_price.net_total_price += (
                product_category_price.price * decimal.Decimal(body["quantity"])
            )
            if cart_price.vat_percent == 0.0:
                cart_price.vat_percent = decimal.Decimal(constants.VAT_PERCENT)
            cart_price.vat_tax_price = cart_price.net_total_price * (
                cart_price.vat_percent * decimal.Decimal(0.01)
            )
            cart_price.total_price = (
                cart_price.net_total_price + cart_price.vat_tax_price
            )
            cart_price.save()
            current_cart_products = CartProductMap.objects.filter(
                cart_id=cart_user.cart_id
            ).all()

            return Response(
                {
                    "status": "success",
                    "data": CartResponseSerializer(
                        {
                            "cart_details": cart,
                            "user_id": self.user.id,
                            "cart_price_details": cart_price,
                            "cart_products": current_cart_products,
                        }
                    ).data["cart_details"],
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": "failure"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    @is_authenticated_user
    def remove_product_from_cart(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product_category = get_object_or_404(
                ProductCategoryMap,
                product_id=body["product_id"],
                category_id=body["category_id"],
            )

            user_query_set = User.objects.filter(id=self.user.id)
            if not user_query_set.exists():
                raise Exception("User data not found")
            user = user_query_set[0]

            cart_user_query_set = CartUserMap.objects.filter(user_id=user.id)
            if not cart_user_query_set.exists():
                raise Exception("Cart-User-Map data not found")
            cart_user = cart_user_query_set[0]

            cart_product_query_set = CartProductMap.objects.filter(
                product_id=product_category.product_id,
                category_id=product_category.category_id,
                cart_id=cart_user.cart_id,
            )
            current_time_in_epoch = int(time.time())

            if not cart_product_query_set.exists():
                return Response(
                    {"status": "success", "message": "Product not found in cart"},
                    status.HTTP_404_NOT_FOUND,
                )

            cart = get_object_or_404(Cart, id=cart_user.cart_id)
            product_category_price = get_object_or_404(
                ProductCategoryPriceMap, product_category_id=product_category.id
            )
            product_category_inventory = get_object_or_404(
                ProductInventoryMap, product_category_id=product_category.id
            )
            cart_price = get_object_or_404(CartPriceMap, cart_id=cart_user.cart_id)

            cart_product = cart_product_query_set[0]
            cart.updated_at = current_time_in_epoch
            cart_product.delete()
            cart.save()

            product_category_inventory.quantity += cart_product.quantity
            cart_price.net_total_price -= (
                product_category_price.price * cart_product.quantity
            )
            cart_price.vat_tax_price = cart_price.net_total_price * (
                cart_price.vat_percent * decimal.Decimal(0.01)
            )
            cart_price.total_price = (
                cart_price.net_total_price + cart_price.vat_tax_price
            )
            product_category_inventory.save()
            cart_price.save()
            current_cart_products = CartProductMap.objects.filter(
                cart_id=cart_user.cart_id
            ).all()

            return Response(
                {
                    "status": "success",
                    "data": CartResponseSerializer(
                        {
                            "cart_details": cart,
                            "user_id": self.user.id,
                            "cart_price_details": cart_price,
                            "cart_products": current_cart_products,
                        }
                    ).data["cart_details"],
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": "failure"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    @is_authenticated_user
    def update_product_count_in_cart(self):
        try:
            body = json.loads(self.body.decode("utf-8"))
            product_category = get_object_or_404(
                ProductCategoryMap,
                product_id=body["product_id"],
                category_id=body["category_id"],
            )

            user_query_set = User.objects.filter(id=self.user.id)
            if not user_query_set.exists():
                raise Exception("User data not found")
            user = user_query_set[0]

            cart_user_query_set = CartUserMap.objects.filter(user_id=user.id)
            if not cart_user_query_set.exists():
                raise Exception("Cart-User-Map data not found")
            cart_user = cart_user_query_set[0]

            cart_product_query_set = CartProductMap.objects.filter(
                product_id=product_category.product_id,
                category_id=product_category.category_id,
                cart_id=cart_user.cart_id,
            )
            current_time_in_epoch = int(time.time())

            if not cart_product_query_set.exists():
                return Response(
                    {"status": "success", "message": "Product not found in cart"},
                    status.HTTP_404_NOT_FOUND,
                )

            cart = get_object_or_404(Cart, id=cart_user.cart_id)
            product_category_price = get_object_or_404(
                ProductCategoryPriceMap, product_category_id=product_category.id
            )
            product_category_inventory = get_object_or_404(
                ProductInventoryMap, product_category_id=product_category.id
            )
            cart_price = get_object_or_404(CartPriceMap, cart_id=cart_user.cart_id)

            cart_product = cart_product_query_set[0]

            if body["add_flag"]:
                if body["quantity"] <= product_category_inventory.quantity:
                    cart_product.quantity += body["quantity"]
                    product_category_inventory.quantity -= body["quantity"]
                    cart_price.net_total_price += (
                        product_category_price.price * decimal.Decimal(body["quantity"])
                    )

                else:
                    return Response(
                        {"status": "success", "message": "Product out of stock"},
                        status=status.HTTP_202_ACCEPTED,
                    )

            else:
                cart_product.quantity -= body["quantity"]
                product_category_inventory.quantity += body["quantity"]
                cart_price.net_total_price -= (
                    product_category_price.price * decimal.Decimal(body["quantity"])
                )

            cart_product.save()
            cart.updated_at = current_time_in_epoch
            cart.save()

            cart_price.vat_tax_price = cart_price.net_total_price * (
                cart_price.vat_percent * decimal.Decimal(0.01)
            )
            cart_price.total_price = (
                cart_price.net_total_price + cart_price.vat_tax_price
            )
            product_category_inventory.save()
            cart_price.save()
            current_cart_products = CartProductMap.objects.filter(
                cart_id=cart_user.cart_id
            ).all()

            return Response(
                {
                    "status": "success",
                    "data": CartResponseSerializer(
                        {
                            "cart_details": cart,
                            "user_id": self.user.id,
                            "cart_price_details": cart_price,
                            "cart_products": current_cart_products,
                        }
                    ).data["cart_details"],
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": "failure"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["POST"])
    @is_authenticated_user
    def checkout_and_place_order(self):
        try:
            user_query_set = User.objects.filter(id=self.user.id)
            if not user_query_set.exists():
                raise Exception("User data not found")
            user = user_query_set[0]

            cart_user_query_set = CartUserMap.objects.filter(user_id=user.id)
            if not cart_user_query_set.exists():
                raise Exception("Cart-User-Map data not found")
            cart_user = cart_user_query_set[0]

            cart_product_query_set = CartProductMap.objects.filter(
                cart_id=cart_user.cart_id
            )
            if not cart_product_query_set.exists():
                return Response(
                    {"status": "success", "message": "Cart is empty"},
                    status.HTTP_200_OK,
                )

            cart_product_list = cart_product_query_set
            cart_price = get_object_or_404(CartPriceMap, cart_id=cart_user.cart_id)

            # create new order
            current_time_in_epoch = int(time.time())
            order_obj_to_save = {
                "cart_id": cart_user.cart_id,
                "total_price": cart_price.total_price,
                "net_total_price": cart_price.net_total_price,
                "vat_percent": cart_price.vat_percent,
                "vat_tax_price": cart_price.vat_tax_price,
                "created_at": current_time_in_epoch,
                "updated_at": current_time_in_epoch,
            }
            order = OrderTable.objects.create(**order_obj_to_save)

            # add products from cart to order
            order_product_list = []
            for product in cart_product_list:
                order_product = OrderProductMap(
                    order_id=order.id,
                    product_id=product.product_id,
                    quantity=product.quantity,
                )
                order_product.save()
                product.delete()
                order_product_list.append(order_product)

            # clear cart and cart price
            reset_zero = decimal.Decimal(0.0)
            cart_price.total_price = reset_zero
            cart_price.net_total_price = reset_zero
            cart_price.vat_percent = reset_zero
            cart_price.vat_tax_price = reset_zero
            cart_price.save()

            current_time_in_epoch = int(time.time())
            cart = get_object_or_404(Cart, id=cart_user.cart_id)
            cart.updated_at = current_time_in_epoch
            cart.save()

            # update user order mapping
            user_order = UserOrderMap(user_id=user.id, order_id=order.id)
            user_order.save()

            # update order status to placed
            current_time_in_epoch = int(time.time())
            order_status = OrderStatus(
                order_id=order.id,
                status=OrderStatusEnum.PLACED.value,
                created_at=current_time_in_epoch,
                updated_at=current_time_in_epoch,
            )
            order_status.save()

            return Response(
                {
                    "status": "success",
                    "message": "Order Placed successfully",
                    "data": OrderResponseSerializer(
                        {
                            "order_details": order,
                            "user_id": self.user.id,
                            "order_status": order_status,
                            "order_products": order_product_list,
                        }
                    ).data["order_details"],
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": "failure"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
