from django.contrib import admin
from .models import Book, User, Reserve, IssueHistory


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_ddc', 'book_name', 'book_img', 'book_author', 'book_publisher', 'book_available', 'book_copies', 'book_category')
    search_fields = ['book_ddc', 'book_name', 'book_author', 'book_publisher', 'book_category']
    list_filter = ['book_ddc', 'book_name']


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'user_email', 'requested_books_display', 'borrowed_books_display')
    search_fields = ['user_id', 'user_name', 'user_email']
    list_filter = ['user_id', 'user_name', 'user_email']
    readonly_fields = ('requested_books_display', 'borrowed_books_display')

    fields = ('user_id', 'user_name', 'user_email', 'user_password', 'requested_books_display', 'borrowed_books_display')

    def requested_books_display(self, obj):
        books = obj.reserve_set.filter(request_status='pending')
        return ", ".join(r.book.book_name for r in books) or "No requested books"
    requested_books_display.short_description = "Requested Books"

    def borrowed_books_display(self, obj):
        books = obj.reserve_set.filter(request_status__in=['ready', 'borrowed'])
        return ", ".join(r.book.book_name for r in books) or "No borrowed books"
    borrowed_books_display.short_description = "Borrowed Books"


class ReserveAdmin(admin.ModelAdmin):
    list_display = ('request_status', 'user', 'book', 'reserved_at', 'reserve_id')
    search_fields = ['user__user_id', 'book__book_name']
    list_filter = ['reserved_at', 'book', 'request_status']
    list_editable = ('request_status',)
    list_display_links = ('user', 'book')

class IssueHistoryAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'user', 'book', 'issue_date', 'return_date')
    search_fields = ['user__user_id', 'book__book_name']
    list_filter = ['issue_date', 'return_date']
    list_display_links = ('user', 'book')


admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Reserve, ReserveAdmin)
admin.site.register(IssueHistory, IssueHistoryAdmin)
