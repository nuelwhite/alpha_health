from django.contrib import admin
from .models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'display_order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_code', 'category', 'organization', 'active')
    list_filter = ('active', 'category', 'organization')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'product_code')