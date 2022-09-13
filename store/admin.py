from pyexpat import model
from typing import Sequence, Union
from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display: Sequence[str] = ['title', 'unit_price','inventory_status','collection_title']
    list_editable: Sequence[str] = ['unit_price']
    list_per_page: int = 10
    list_select_related: Union[bool, Sequence[str]] = ['collection']

    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'Ok'

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name','payment_status','placed_at','id']
    list_per_page: int = 10
    list_select_related: Union[bool, Sequence[str]] = ['customer']
    
    @admin.display(ordering='customer')
    def customer_name(self, order):
        return order.customer.first_name + " "+ order.customer.last_name

    
    

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','membership']
    list_editable: Sequence[str] = ['membership']
    list_per_page: int = 10

# Register your models here.
admin.site.register(models.Collection)
