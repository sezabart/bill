from django.contrib import admin

from .models import Printer, Location, ProductCategory, Product

admin.site.register(Printer)
admin.site.register(Location)
admin.site.register(ProductCategory)
admin.site.register(Product)
