from django.contrib import admin

from .models import (Product, Category, Store, ProductsInStore, Discount, 
                    StoreLocation, ChainStore)

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Store)

admin.site.register(ProductsInStore)
admin.site.register(Discount)
admin.site.register(StoreLocation)
admin.site.register(ChainStore)