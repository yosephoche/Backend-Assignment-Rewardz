from django.contrib import admin

from book.models import Book, Transaction, TransactionDetail


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "id", "title", "author", "publisher", "year", "description", "stock",
    ]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "trx_type"]


@admin.register(TransactionDetail)
class TransactionDetailAdmin(admin.ModelAdmin):
    list_display = [
        "fk_transaction",
        "is_renew",
        "return_deadline",
        "is_returned",
    ]
