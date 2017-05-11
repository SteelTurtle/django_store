from django.contrib import admin

from .models import Post


# let's customize the views on the Admin site
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publication_date')
    search_fields = ('title', 'slug')
    list_filter = ('publication_date', 'tags')
    date_hierarchy = 'publication_date'
    filter_horizontal = ('products',)


admin.site.register(Post, BlogAdmin)
