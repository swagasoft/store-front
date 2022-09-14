
from typing import Any, Dict, List, Sequence, Tuple, Union
from django.contrib import admin

from django.http.request import HttpRequest

from . import models
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.utils.html import format_html, urlencode
from django.utils.http import urlencode
from django.urls import reverse


class InventoryFilter(admin.SimpleListFilter):
    title: str = 'inventory'
    parameter_name: str = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [('<10', 'Low')]

    def queryset(self, request: Any, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields: Sequence[str] = ['title']
    # inlines = [TagInline]
    autocomplete_fields: Sequence[str] = ['collection']
    prepopulated_fields: Dict[str, Sequence[str]] = {'slug':['title']}
    list_display: Sequence[str] = ['title', 'unit_price','inventory_status','collection_title']
    list_editable: Sequence[str] = ['unit_price']
    list_per_page: int = 10
    actions = ['clear_inventory']
    list_filter = ['collection','last_update', InventoryFilter]
    list_select_related: Union[bool, Sequence[str]] = ['collection']

    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'Ok'

    @admin.action(description='clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count =  queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated!')

class OrderItemInline(admin.TabularInline):
    autocomplete_fields: Sequence[str] = ['product']
    model =  models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields: Sequence[str] = ['customer']
    list_display = ['customer_name','payment_status','placed_at','id']
    list_per_page: int = 10
    list_select_related: Union[bool, Sequence[str]] = ['customer']
    
    @admin.display(ordering='customer')
    def customer_name(self, order):
        return order.customer.first_name + " "+ order.customer.last_name

    
    

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','membership', 'order_count']
    list_editable: Sequence[str] = ['membership']
    list_per_page: int = 10
    # search_fields: Sequence[str] = ['first_name', 'last_name']
    # search_fields: Sequence[str] = ['first_name__startswith', 'last_name__startswith']
    search_fields: Sequence[str] = ['first_name__istartswith', 'last_name__istartswith']
    
    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = (reverse('admin:store_order_changelist') +
        '?' + urlencode({'customer__id': str(customer.id)}) )
        return  format_html('<a href="{}"> {} </a>', url, customer.order_count )

    def get_queryset(self, request: HttpRequest) :
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )



@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields: Sequence[str] = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
         + '?' + urlencode({'collection__id': str(collection.id)}) )
        return format_html('<a href="{}" >{} </a>', url, collection.products_count)
        

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            products_count= Count('product')
        )
