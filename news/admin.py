from django.contrib import admin
from .models import Category, Article, Comment

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "views", "is_active", "category", "author")
    list_display_links = ("pk", "title")
    list_editable = ("is_active", "category", "author")
    list_filter = ("is_active", "category", "author")


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)

