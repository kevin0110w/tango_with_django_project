from django.contrib import admin
from rango.models import Category, Page

# Register your models here.

# admin.site.register(Category)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

admin.site.register(Page, PageAdmin)

# customise Admin Integerface

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# update the registration to include the customised interface

admin.site.register(Category, CategoryAdmin)