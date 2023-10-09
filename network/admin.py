from django.contrib import admin
from .models import User, Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("likes",)
    list_display = ("id", "user", "body", )

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("followers", "following", )
    

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)