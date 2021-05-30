from django.contrib import admin
from products.models import Product1

# Register your models here.
class Product1Admin(admin.ModelAdmin):
    list_display = ("id","sku", "name", "tax_code", "purchase_price", "mrp", "hsn")

admin.site.register(Product1, Product1Admin)