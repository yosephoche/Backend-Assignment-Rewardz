from datetime import datetime
from dateutil.relativedelta import relativedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.response import Response

from book.filters import BookListFilter
from book.serializers import ListCreateBookSerializer, BookBaseSerializer, BorrowBookSerializer, \
    BorrowBookResponseSerializer

from book.models import Book, Transaction, TransactionDetail


class BookListView(ListCreateAPIView):
    permission_classes = []
    serializer_class = ListCreateBookSerializer
    queryset = Book.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookListFilter


class BorrowView(GenericAPIView):
    permission_classes = []

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BorrowBookSerializer
        return BorrowBookResponseSerializer

    def post(self, request):
        payload = request.data
        book_id_list = payload.pop("books")
        transaction = Transaction.objects.create(**payload)
        return_deadline = datetime.now() + relativedelta(months=+1)

        transaction_borrow_dict = {
            "trx_id": "",
            "details": []
        }
        for book_id in book_id_list:
            book = Book.objects.filter(id=book_id).first()

            transaction_detail = TransactionDetail.objects.create(
                book=book,
                fk_transaction=transaction,
                return_deadline=return_deadline
            )

            transaction_borrow_dict["details"].append(transaction_detail)

        serializer = BorrowBookResponseSerializer(transaction_borrow_dict)

        return Response(serializer.data)

    def get(self, request):
        pass
