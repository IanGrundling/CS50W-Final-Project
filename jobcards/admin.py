from django.contrib import admin
from .models import User, Customer, Product, Jobcard, JobcardItem, JobcardId

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Jobcard)
admin.site.register(JobcardItem)
admin.site.register(JobcardId)