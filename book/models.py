from django.db import models

from library_system.behaviors import Timestampable


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

