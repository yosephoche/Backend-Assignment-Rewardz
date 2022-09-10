from django.db import models

from authentication.models import User
from library_system.behaviors import Timestampable, UserAwareModel


class Book(Timestampable, models.Model):
    title = models.CharField("Title", max_length=200)
    author = models.CharField("Author", max_length=100)
    publisher = models.CharField("Publisher", max_length=100)
    year = models.CharField("Year", max_length=50)
    description = models.TextField()
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class BookAwareModel(Timestampable, models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Transaction(UserAwareModel):
    TRX_TYPE_BORROWED = 'borrowed'
    TRX_TYPE_RETURNED = 'returned'

    TRX_TYPE = (
        (TRX_TYPE_BORROWED, 'borrowed'),
        (TRX_TYPE_RETURNED, 'returned'),
    )

    trx_type = models.CharField(max_length=50, choices=TRX_TYPE)
    borrowed_at = models.DateTimeField()
    returned_at = models.DateTimeField()


class TransactionDetail(BookAwareModel):
    fk_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    is_renew = models.BooleanField(default=False)
    return_deadline = models.DateTimeField()
