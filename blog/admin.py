from django.contrib import admin
from .models import *


# admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Image)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name', 'order', 'active', 'megamenu')
    ordering = ('parent', 'order', 'name')
    # list_editable = ('parent', 'name', 'order')

# Registrar a model e a classe de administração personalizada
admin.site.register(Category, CategoryAdmin)
