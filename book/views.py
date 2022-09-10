from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView

from book.filters import BookListFilter
from book.serializers import ListCreateBookSerializer

from book.models import Book


class BookListView(ListCreateAPIView):
    permission_classes = []
    serializer_class = ListCreateBookSerializer
    queryset = Book.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookListFilter
