from django.db import models

# Create your models here.
class Product1(models.Model):
    name = models.CharField(max_length=256)
    sku = models.CharField(max_length=32, unique=True)
    brand = models.CharField(max_length=16, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_code = models.IntegerField()
    hsn = models.CharField(max_length=16, blank=True, null=True)