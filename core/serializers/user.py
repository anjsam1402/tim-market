import json
from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "is_superuser",
            "username",
            "name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
        ]


class UserResponseSerializer(serializers.Serializer):
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["user_details"]

    def get_user_details(self, obj):
        user_data = UserSerializer(obj["user_details"]).data
        user_data["cart_id"] = obj["cart_id"]
        return user_data
