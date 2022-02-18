from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile
# Register your models here.

# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category','url')
  #admin.site.register(Page, PageAdmin) in Rango’s admin.py file

# Update the registration to include this customised interface
admin.site.register(Category, CategoryAdmin)
#admin.site.register(Category)
admin.site.register(Page,PageAdmin)

admin.site.register(UserProfile)
  