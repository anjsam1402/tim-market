from django.db import models


class OrderStatusEnum(models.TextChoices):
    PLACED = "placed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERD = "delivered"
