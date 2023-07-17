from core.decorators import is_authenticated_user, is_user_admin
from core.serializers.user import UserResponseSerializer, UserSerializer
from core.services.cart import CartService
from ..models import User
from ..models import Cart, CartUserMap
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import json
from datetime import datetime
from django.utils import timezone


class UserService:

    """
    User Service has the following list of operations:
    - all CRUD Operations related to User

    Currently this service focuses on following requirements:
    - a user can have only one cart {for now}, we will do the following while creation of user :
        - create the cart
        - create cart and user mapping
        - cart and initial cart-price mapping

    This logic should be moved out with scaling of the application requirement.
    """

    def create_cart_data(user):
        created_at_in_epoch = datetime.now().strftime("%s")
        cart_json_obj = {
            "created_at": created_at_in_epoch,
            "updated_at": created_at_in_epoch,
        }
        cart, _ = CartService.create_new_cart_object(cart_json_obj)

        cart_user = CartUserMap(cart_id=cart.id, user_id=user.id, platform="web")
        cart_user.save()
        return cart_user

    @api_view(["POST"])
    def create_user(self):
        try:
            body = json.loads(self.body.decode("utf-8"))

            if "is_staff" not in body:
                body["is_staff"] = False
            if "is_active" not in body:
                body["is_active"] = True
            if "date_joined" not in body:
                body["date_joined"] = timezone.now()

            user = User.objects.create(**body)
            cart_user = UserService.create_cart_data(user)

            return Response(
                {
                    "status": "success",
                    "data": UserResponseSerializer(
                        {"user_details": user, "cart_id": cart_user.cart_id}
                    ).data["user_details"],
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
    def get_user(self, id):
        try:
            user = User.objects.get(id=id)
            cart_user_query_set = CartUserMap.objects.filter(user_id=id)
            if not cart_user_query_set.exists():
                raise Exception("Cart-User data not found")
            cart_user = cart_user_query_set[0]

            return Response(
                {
                    "status": "success",
                    "data": UserResponseSerializer(
                        {"user_details": user, "cart_id": cart_user.cart_id}
                    ).data["user_details"],
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["GET"])
    @is_authenticated_user
    def get_all_user(self):
        try:
            users = User.objects.all()

            response_list = []
            for user in users:
                cart_user_query_set = CartUserMap.objects.filter(user_id=user.id)
                if not cart_user_query_set.exists():
                    raise Exception("Cart-User data not found")
                cart_user = cart_user_query_set[0]
                response_list.append(
                    UserResponseSerializer(
                        {"user_details": user, "cart_id": cart_user.cart_id}
                    ).data["user_details"]
                )

            return Response(
                {"status": "success", "data": response_list},
                status.HTTP_200_OK,
            )
        except Exception as e:
            print("Exception logged: ", e)
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["PATCH"])
    def update_user(self, id):
        try:
            body = json.loads(self.body.decode("utf-8"))
            user = User.objects.get(id=id)
            for key in body:
                setattr(user, key, body[key])
            user.save()

            cart_user_query_set = CartUserMap.objects.filter(user_id=user.id)
            if not cart_user_query_set.exists():
                raise Exception("Cart-User data not found")
            cart_user = cart_user_query_set[0]

            return Response(
                {
                    "status": "success",
                    "data": UserResponseSerializer(
                        {"user_details": user, "cart_id": cart_user.cart_id}
                    ).data["user_details"],
                },
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(["DELETE"])
    @is_user_admin
    def delete_user(self, id):
        """
        Restricted for admin use
        """
        try:
            user = User.objects.get(id=id)
            user.delete()

            cart_user_data_list = CartUserMap.objects.filter(user_id=id).all()
            for cart_user_data in cart_user_data_list:
                cart = Cart.objects.get(id=cart_user_data.cart_id)
                cart.delete()
                cart_user_data.delete()

            return Response(
                {"status": "success", "message": "User and cart details deleted"},
                status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"status": "failure"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
