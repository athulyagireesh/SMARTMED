from .models import Product , Order , OrderItem
from django.contrib import admin

admin.site.register(Product)


# ✅ Show items inside each order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# ✅ Order Admin Panel
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'total_amount',
        'payment_method',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'payment_method'
    )

    search_fields = (
        'user__username',
        'id'
    )

    inlines = [OrderItemInline]


# ✅ Register Order
admin.site.register(Order, OrderAdmin)