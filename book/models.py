from django.db import models

from authentication.models import UserAwareModel
from book.managers import BookManager, TransactionDetailManager
from library_system.behaviors import Timestampable


class Book(Timestampable, models.Model):
    title = models.CharField("Title", max_length=200)
    author = models.CharField("Author", max_length=100)
    publisher = models.CharField("Publisher", max_length=100)
    year = models.CharField("Year", max_length=50)
    description = models.TextField()
    stock = models.IntegerField(default=1)

    objects = BookManager

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        total_borrowed_book = TransactionDetail.objects.count_borrowed_book(self.id)
        return self.stock > total_borrowed_book

    @property
    def returned_at(self):
        if self.is_available:
            return None

        transaction_detail = TransactionDetail.objects.filter(book=self).order_by("-created_at").first()
        return transaction_detail.return_deadline.strftime("%b %d %Y %H:%M:%S")


class BookAwareModel(Timestampable, models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Transaction(UserAwareModel):
    TRX_TYPE_BORROW = 'borrow'
    TRX_TYPE_RETURN = 'return'

    TRX_TYPE = (
        (TRX_TYPE_BORROW, 'borrow'),
        (TRX_TYPE_RETURN, 'return'),
    )

    STATUS_ONGOING = "ongoing"
    STATUS_COMPLETE = "complete"

    TRX_STATUS = (
        (STATUS_ONGOING, "ongoing"),
        (STATUS_COMPLETE, "complete"),
    )

    trx_type = models.CharField(max_length=50, choices=TRX_TYPE)
    status = models.CharField(max_length=50, choices=TRX_STATUS, blank=True, null=True)


class TransactionDetail(BookAwareModel, models.Model):
    fk_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    is_renew = models.BooleanField(default=False)
    return_deadline = models.DateTimeField(null=True)
    is_returned = models.BooleanField(default=False)

    objects = TransactionDetailManager()

