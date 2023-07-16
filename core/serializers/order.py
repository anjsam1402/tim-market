from rest_framework import serializers
from ..models import OrderProductMap, OrderStatus, OrderTable


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductMap
        fields = "__all__"


class OrderTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTable
        fields = "__all__"


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = "__all__"


class OrderResponseSerializer(serializers.Serializer):
    order_details = serializers.SerializerMethodField()

    class Meta:
        model = OrderTable
        fields = ["order_details"]

    def get_order_details(self, obj):
        order_data = OrderTableSerializer(obj["order_details"]).data
        order_id = order_data["id"]
        order_data["user_id"] = obj["user_id"]
        order_data.update(**(OrderStatusSerializer(obj["order_status"])).data)
        order_data["order_products"] = OrderProductSerializer(
            obj["order_products"], many=True
        ).data
        order_data["id"] = order_id

        return order_data
