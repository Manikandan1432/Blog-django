from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    list_filter = ('title',)
    search_fields = ('title', 'created_at')
    ordering = ('-title',)
    list_editable = ('content',)
    fields = ('title', 'content')
    list_display_links = ()

admin.site.register(Category)
admin.site.register(Datas, PostAdmin)
admin.site.register(AboutUs)
admin.site.site_header = 'Blog Admin'
admin.site.site_title = 'Blog Admin Portal'
admin.site.index_title = 'Welcome to Blog Administration'