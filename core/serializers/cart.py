from rest_framework import serializers
from core.models import Cart, CartPriceMap, CartProductMap, CartUserMap


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartPriceMap
        fields = "__all__"


class CartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartUserMap
        fields = "__all__"


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProductMap
        fields = "__all__"


class CartResponseSerializer(serializers.Serializer):
    cart_details = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["cart_details"]

    def get_cart_details(self, obj):
        cart_data = CartSerializer(obj["cart_details"]).data
        cart_id = cart_data["id"]
        cart_data["user_id"] = obj["user_id"]
        cart_data.update(**(CartPriceSerializer(obj["cart_price_details"])).data)
        cart_data["cart_products"] = CartProductSerializer(
            obj["cart_products"], many=True
        ).data
        cart_data["id"] = cart_id

        return cart_data
