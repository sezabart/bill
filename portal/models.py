from django.db import models

# Create your models here.

class Printer(models.Model):
    name = models.CharField(max_length=255)
    # Remote
    ip = models.GenericIPAddressField(null=True, blank=True)
    port = models.PositiveIntegerField(null=True, blank=True)
    # Local
    device = models.CharField(max_length=255, null=True, blank=True)
    
    
    def print_text(self, text):
        # Check if text is printable
        if not text:
            raise ValueError('Text is empty')
        if self.ip and self.port:
            # Send text to remote printer
            # TODO: implement remote printing
            print(f'Printing on {self.ip}:{self.port}: {text}')
            return True # TODO: return status
        elif self.device:
            # Send text to local printer
            # TODO: implement local device printing
            print(f'Printing on {self.device}: {text}')
            return True # TODO: return status
        else:
            raise ValueError('Either remote or local should be provided')

    
    def clean(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        # Validation, either remote or local should be provided
        if not (self.ip and self.port) and not self.device:
            raise ValidationError('Either remote or local should be provided')
        elif (self.ip and self.port) and self.device:
            raise ValidationError('Only remote OR local should be provided')
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=255)
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Bill(models.Model):
    customer = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False)
    # customer
    # mentor

    def __str__(self):
        return f'{self.customer} - {self.date}'
    
    @property
    def num_items(self):
        return self.bill_items.count()
    
    @property
    def sum_amount(self):
        return sum([item.amount() for item in self.bill_items.all()])

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='bill_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bill_items')
    quantity = models.FloatField()

    def __str__(self):
        return f'{self.product} - {self.quantity}'
    
    def amount(self):
        return self.product.price_per_unit * self.quantity