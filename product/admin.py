from django.contrib import admin

from .models import Link, Product, Tag


# let's customize the views on the Admin site
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'added_to_catalogue')
    search_fields = ('name', 'slug')
    list_filter = ('added_to_catalogue', 'tags')


admin.site.register(Link)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
