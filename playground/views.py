from decimal import Decimal
from itertools import product
from operator import concat, contains
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F,Value,Func, ExpressionWrapper
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Product, Customer, Collection, OrderItem, Order
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db import transaction, connection



def say_hello(request):
  
    # products = Product.objects.filter(unit_price__gt = 20)
    # queryset = Product.objects.filter(unit_price__range =(20, 30))
    # queryset = Product.objects.filter(title__contains='coffee')
    # queryset = Product.objects.filter(title__icontains='coffee')
    # queryset = Product.objects.filter(title__startswith='Coffee')
    # queryset = Product.objects.filter(title__endswith='Coffee')
    # queryset = Product.objects.filter(last_update__year=2021)
    # queryset = Product.objects.filter(inventory__lt=10)
    # customers = Customer.objects.filter(email__endswith='.com') # customers email ends with .com
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)) # and operator
    # queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20)) # and not operator
    # queryset = Product.objects.filter(inventory=F('unit_price')) # Reference fields using F objects
    # queryset = Product.objects.order_by('unit_price', '-title') #  order by
    # queryset = Product.objects.all()[0:5] #  limiting items
    # queryset = Product.objects.values('id', 'unit_price', 'collection__title')[0:10] #  limiting items
    # queryset = Product.objects.values_list('id', 'unit_price', 'collection__title')[0:10] #  limiting items
    # queryset = Product.objects.filter(id__in= OrderItem.objects.values('product_id').distinct()).order_by('unit_price')
    # use select related when the other end of the relationship has 1 instance
    # use pre fetch when the other end of the relationship has many object
    # queryset = Product.objects.select_related('collection').all()
    # queryset = Product.objects.prefetch_related('promotions').all()
    # queryset = Product.objects.prefetch_related('promotions').select_related('collection').all()
    #  select order and order items and customer who place the order, limit by 5
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product') .order_by('-placed_at')[0:5]
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    # how many order do we have
    # result = Order.objects.aggregate(Count('id'))
    # How many unit of product 1 have we sold?
    # result = OrderItem.objects.filter(product__id=1).aggregate(Count('id'))
    #  How many order has customer 1 placed?
    # result = Order.objects.filter(customer__id=1).aggregate(Count('id'))
    # what is the Min, max and Avg of product of collection 1
    # result = Product.objects.filter(collection__id=3).aggregate(
    #     min_price=Min('unit_price'),
    #     average_price=Avg('unit_price'),
    #     maximum_price=Max('unit_price'),
    # )
    # print('Note ', list(queryset.values()))
    # queryset = Customer.objects.annotate(is_new=Value(True))
    # queryset = Customer.objects.annotate(new_id=F('id'))
    # queryset = Customer.objects.annotate(new_id=F('id') + 1)
    # queryset = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'),function='CONCAT'))
    # queryset = Customer.objects.annotate(full_name=Concat('first_name', Value(' '),'last_name'))
    # queryset = Customer.objects.annotate(order_count=Count('order'))
    collection = Collection.objects.get(pk=11)
    collection.featured_product = None
    collection.save()
  

    return render(request, 'hello.html',{'name':'simon J'})
