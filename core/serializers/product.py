from core.models import (
    Category,
    Product,
    ProductCategoryMap,
    ProductCategoryPriceMap,
    ProductInventoryMap,
)
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryMap
        fields = "__all__"


class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryMap
        fields = "__all__"


class ProductCategoryPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryPriceMap
        fields = "__all__"


class ProductCategoryResponseSerializer(serializers.Serializer):
    product_category_details = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["product_category_details"]

    def get_product_category_details(self, obj):
        product_category_data = {}
        category_data = CategorySerializer(obj["category_details"]).data
        product_category_data["category_id"] = category_data["id"]
        product_category_data["category_name"] = category_data["name"]
        product_category_data.update(
            **(
                ProductCategoryPriceSerializer(obj["product_category_price_details"])
            ).data
        )
        product_category_data.update(
            **(ProductInventorySerializer(obj["product_inventory_details"])).data
        )
        product_category_data.pop("id", None)
        return product_category_data


class ProductResponseSerializer(serializers.Serializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["product_details"]

    def get_product_details(self, obj):
        product_data = ProductSerializer(obj["product_details"]).data
        product_data["category_details"] = obj["category_details"]

        return product_data
