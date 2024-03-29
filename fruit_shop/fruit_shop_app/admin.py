from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (
    User,
    Category,
    Product,
    Employee,
    Customer,
    Order,
    OrderItem,
    Supplier,
    Transaction,
    Discount,
    StoreLocation,
    Address,
)


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Supplier)
admin.site.register(Transaction)
admin.site.register(Discount)
admin.site.register(StoreLocation)
admin.site.register(Address)
