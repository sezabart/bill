from django.db import models

# Create your models here.

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

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bills')
    timestamp = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.customer} - {self.date}'
    
    def total_amount(self):
        return sum([item.amount() for item in self.bill_items.all()])

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='bill_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bill_items')
    quantity = models.PositiveIntegerField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.product} - {self.quantity}'
    
    def amount(self):
        return self.product.price_per_unit * self.quantity