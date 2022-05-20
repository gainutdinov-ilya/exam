from django.contrib import admin

import demo.forms
from demo.models import *


# Register your models here.


class OrderItems(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = demo.forms.OrderForm
    inlines = [OrderItems]


admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
