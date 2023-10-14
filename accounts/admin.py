from django.contrib import admin
from .models import *


#class CustomUserAdmin(admin.ModelAdmin):
    #list_display = ('username', 'email', 'user_type','date_posted')
    #list_filter = ("user_type",)
    #search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(CustomUser)
#admin.site.register(CustomUser, CustomUserAdmin)