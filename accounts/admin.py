from django.contrib import admin
from core.models import *


#class CustomUserAdmin(admin.ModelAdmin):
    #list_display = ('username', 'email', 'user_type','date_posted')
    #list_filter = ("user_type",)
    #search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(CustomUser)
admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(ExpertPortfolio)

#admin.site.register(CustomUser, CustomUserAdmin)