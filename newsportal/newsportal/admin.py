from django.contrib import admin
from .models import Post, Author, Category


class CategoryInline(admin.TabularInline):
    model = Category.posts.through


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [
        CategoryInline,
    ]


admin.site.register(Author)
