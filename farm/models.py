# farm/models.py
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Crop(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('Growing', 'Growing'),
        ('Harvested', 'Harvested'),
        ('Failed', 'Failed'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True)
    acres = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    season = models.CharField(max_length=50)
    start_date = models.DateField()
    expected_harvest_date = models.DateField(null=True, blank=True)
    actual_harvest_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.variety}) - {self.farmer.username}"


class CropExpense(models.Model):
    CATEGORY_CHOICES = [
        ('seeds', 'Seeds'),
        ('fertilizer', 'Fertilizer'),
        ('pesticides', 'Pesticides'),
        ('labour', 'Labour'),
        ('tractor', 'Tractor/Ploughing'),
        ('irrigation', 'Irrigation/Electricity'),
        ('equipment', 'Equipment Rental'),
        ('transport', 'Transport'),
        ('harvesting', 'Harvesting'),
        ('other', 'Other'),
    ]

    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='expenses')
    expense_date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    description = models.TextField(blank=True)
    quantity = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.category} - {self.amount} for {self.crop.name}"


class Harvest(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='harvests')
    harvest_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    unit = models.CharField(max_length=20, default='kg')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} harvested on {self.harvest_date}"


class CropSale(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='sales')
    harvest = models.ForeignKey(Harvest, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    sale_date = models.DateField()
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    buyer = models.CharField(max_length=100, blank=True)
    selling_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0)])

    @property
    def sales_revenue(self):
        quantity = Decimal(str(self.quantity_sold))
        unit_price = Decimal(str(self.unit_price))
        selling_cost = Decimal(str(self.selling_cost or 0))
        return (quantity * unit_price) - selling_cost

    def __str__(self):
        return f"Sale of {self.quantity_sold} from {self.crop.name}"