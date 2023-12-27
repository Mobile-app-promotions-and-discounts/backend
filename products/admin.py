from django.contrib import admin

from .models import (Category, ChainStore, Discount, Favorites, Product,
                     ProductImage, Review, Store, StoreLocation)


class StoreInline(admin.TabularInline):
    model = Product.stores.through


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    list_display = ('image',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')
    list_filter = ('product',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        StoreInline,
    ]
    exclude = ['stores']
    list_display = ('name', 'category',)
    list_filter = ('category', )
    search_fields = ('name', 'id')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name', 'id')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'chain_store',)
    list_filter = ('name', 'chain_store')
    search_fields = ('name', 'id', 'chain_store')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_rate', 'discount_unit', 'discount_start', 'discount_end', 'discount_card')
    list_filter = ('discount_rate',)


@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ('region', 'city', 'address',)
    list_filter = ('city',)


@admin.register(ChainStore)
class ChainStoreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('product', 'user')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'text', 'score', 'pub_date')
    list_filter = ('product',)
    search_fields = ('product', 'pub_date')
