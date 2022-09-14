from typing import Sequence
from django.db import models
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin



# Create your models here.
class TagInline(GenericTabularInline):
    autocomplete_fields: Sequence[str] = ['tag']
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    search_fields: Sequence[str] = [TagInline]

admin.site.unregister(Product)
admin.site.register( Product,CustomProductAdmin)


