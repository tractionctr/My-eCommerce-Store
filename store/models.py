"""Database models for the store application."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from decimal import Decimal


def clean_price(value):
    """Safely convert a value to Decimal price format."""
    try:
        return Decimal(str(value))
    except (ValueError, TypeError, ArithmeticError):
        return Decimal("0.00")


class User(AbstractUser):
    """Custom user model with vendor role support."""
    is_vendor = models.BooleanField(default=False)


class Store(models.Model):
    """Represents a vendor store."""
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Represents a product sold in a store."""
    def __str__(self):
        return self.name

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MaxValueValidator(Decimal("999999"))]
    )


class Order(models.Model):
    """Represents a customer order."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    """Represents a product review."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    content = models.TextField()
