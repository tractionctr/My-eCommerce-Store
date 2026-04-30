from django.contrib import admin
from .models import User, Store, Product, Order, Review

# Register your models
admin.site.register(User)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review)
