from typing import Sequence
from django.contrib import admin
from .models import Tag

# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields: Sequence[str] = ['label']
