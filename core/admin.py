from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Pricing)
admin.site.register(Subscription)
admin.site.register(Product)
admin.site.register(Employee)
admin.site.register(AdminProfile)
admin.site.register(EmployeeProfile)
admin.site.register(ExpertProfile)
admin.site.register(CompanyProfile)
admin.site.register(Industry)
admin.site.register(Sectors)
admin.site.register(FicheTechnic)    
admin.site.register(Jobs)
admin.site.register(JobApplication)
admin.site.register(Testimonies)
admin.site.register(Deals)
admin.site.register(Rfi)
admin.site.register(Experts)
admin.site.register(Enterprises)
admin.site.register(Education)
admin.site.register(Trainings)
admin.site.register(TrainingApplication)

class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blog, BlogAdmin)
admin.site.register(Review)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)