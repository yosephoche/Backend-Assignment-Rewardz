from rest_framework import serializers

from book.models import Book


class BookBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ListCreateBookSerializer(BookBaseSerializer):
    pass
