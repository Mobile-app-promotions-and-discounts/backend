from django.contrib import admin
from .models import Category


from .models import Category, ChainStore, Discount, Product, ProductImage, Store, StoreLocation


class StoreInline(admin.TabularInline):
    model = Product.store.through


class ImageInline(admin.TabularInline):
    model = Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        StoreInline,
    ]
    exclude = ['store']
    list_display = ('name', 'category', 'price',)
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


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('main_image', 'additional_photo',)


@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ('region', 'city', 'street', 'building',)
    list_filter = ('city',)


@admin.register(ChainStore)
class ChainStoreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
