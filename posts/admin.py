from django.contrib import admin
from .models import Author, Post, Catagory, Comment, PostView, Tag, SavedPost
# Register your models here.

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Catagory)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(Tag)
admin.site.register(SavedPost)


