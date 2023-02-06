from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Customer(models.Model):
    cust_name = models.CharField(max_length=255)
    cust_surname = models.CharField(max_length=255)
    cust_number = models.CharField(blank=True, max_length=10)
    cust_email = models.EmailField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer {self.cust_name}"

class Product(models.Model):
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = models.FloatField(max_length=11)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.manufacturer}, {self.model}"

class Jobcard(models.Model):
    installer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    jobcard_id = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.id}: {self.customer}"

    @property
    def get_item_total(self):
        jobcarditems = self.jobcarditem_set.all()
        total = sum([item.get_total for item in jobcarditems])
        return total
    
    @property
    def get_jobcard_items(self):
        jobcarditems = self.jobcarditem_set.all()
        total = sum([item.quantity for item in jobcarditems])
        return total

class JobcardItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    jobcard = models.ForeignKey(Jobcard, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f"{self.product} added to jobcard {self.jobcard}"

class JobcardId(models.Model):
    jc_id = models.IntegerField()