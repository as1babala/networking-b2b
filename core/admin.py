from django.contrib import admin
from .models import *
#from networking.urls import *

# Register your models here.
admin.site.register(Pricing)
#admin_site.register(Pricing)
admin.site.register(Subscription)
admin.site.register(Product)
#admin.site.register(Employee)
admin.site.register(AdminProfile)
admin.site.register(EmployeeProfile)
admin.site.register(ExpertProfile)
admin.site.register(ExpertMessaging)
#admin.site.register(CompanyProfile)
admin.site.register(Industry)
admin.site.register(Sectors)
admin.site.register(FicheTechnic)    
admin.site.register(Jobs)
admin.site.register(JobApplication)
admin.site.register(Testimonies)
admin.site.register(Deals)#services related deals
admin.site.register(DealImages)
admin.site.register(Rfi)
admin.site.register(ProductDeals)
admin.site.register(ProductDealImages)
admin.site.register(ProductRFI)
#admin.site.register(Experts)
admin.site.register(Enterprises)
#admin.site.register(Education)
admin.site.register(Trainings)
admin.site.register(TrainingApplication)

class BlogAdmin(admin.ModelAdmin):
     list_display=['categories','title','author', 'status', 'created_on']
   
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogRead)
admin.site.register(Review)
admin.site.register(ReplyToReview)

class ForumAdmin(admin.ModelAdmin):
     list_display=['category','topic','active', 'created_on']
     
admin.site.register(Forum, ForumAdmin)
admin.site.register(Discussion)


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)