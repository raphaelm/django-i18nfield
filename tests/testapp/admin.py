from django.contrib import admin

from .forms import BookForm
from .models import Author, Book


class BookAdmin(admin.ModelAdmin):
    form = BookForm


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
