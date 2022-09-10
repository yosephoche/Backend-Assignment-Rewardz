from datetime import datetime
from dateutil.relativedelta import relativedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.response import Response

from book.exceptions import BookOutOfStock, MaxBorrowedReach
from book.filters import BookListFilter, TransactionListFilter
from book.serializers import ListCreateBookSerializer, BookBaseSerializer, BorrowBookSerializer, \
    BorrowBookResponseSerializer, TransactionDetailListSerializer, TransactionListSerializer

from book.models import Book, Transaction, TransactionDetail
from library_system.constants import MAX_BORROWED_BOOK


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
        user_id = payload.get("fk_user_id")
        transaction = Transaction.objects.create(**payload)
        return_deadline = datetime.now() + relativedelta(months=+1)

        total_borrowed_book_by_student = TransactionDetail.objects.count_borrowed_book_by_student(user_id)

        if total_borrowed_book_by_student == MAX_BORROWED_BOOK:
            raise MaxBorrowedReach()

        transaction_borrow_dict = {
            "trx_id": "",
            "details": []
        }

        for book_id in book_id_list:
            book = Book.objects.filter(id=book_id).first()

            if not book.is_available:
                raise BookOutOfStock()

            transaction_detail = TransactionDetail.objects.create(
                book=book,
                fk_transaction=transaction,
                return_deadline=return_deadline
            )

            transaction_borrow_dict["details"].append(transaction_detail)

        serializer = BorrowBookResponseSerializer(transaction_borrow_dict)

        return Response(serializer.data)


class StudentBorrowList(ListAPIView):
    permission_classes = []
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionListFilter

