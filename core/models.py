from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CoreUserManager


class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128)
    username = models.CharField(unique=True, max_length=150)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CoreUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "email"]

    class Meta:
        # db_table = 'core_user'
        managed = False

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0]


class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.IntegerField()
    updated_at = models.IntegerField()

    class Meta:
        managed = False
        db_table = "cart"


class CartPriceMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart_id = models.BigIntegerField(unique=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    net_total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    vat_percent = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    vat_tax_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "cart_price_map"


class CartProductMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField(blank=True, null=True)
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "cart_product_map"


class CartUserMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    platform = models.CharField(max_length=26, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cart_user_map"


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "category"


class OrderProductMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.BigIntegerField()
    order_id = models.BigIntegerField()
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "order_product_map"
        unique_together = (("order_id", "product_id"),)


class OrderStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.BigIntegerField(unique=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.IntegerField()
    updated_at = models.IntegerField()

    class Meta:
        managed = False
        db_table = "order_status"


class OrderTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart_id = models.BigIntegerField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    net_total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    vat_percent = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    vat_tax_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "order_table"


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "product"


class ProductCategoryMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.IntegerField()
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "product_category_map"
        unique_together = (("product_id", "category_id"),)


class ProductCategoryPriceMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_category_id = models.IntegerField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "product_category_price_map"


class ProductInventoryMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_category_id = models.IntegerField(unique=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "product_inventory_map"


class UserOrderMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    order_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "user_order_map"
        unique_together = (("user_id", "order_id"),)
