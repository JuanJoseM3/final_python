from django.contrib import admin
from .models import Author, Rack, Book, BookItem

# Register your models here.

admin.site.register(Author)
admin.site.register(Rack)
admin.site.register(Book)
admin.site.register(BookItem)