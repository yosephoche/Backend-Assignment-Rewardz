from datetime import datetime
from dateutil.relativedelta import relativedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from book.exceptions import BookOutOfStock, MaxBorrowedReach, BookAlreadyBorrowed, AlreadyRenewed, RenewedDisallowed
from book.filters import BookListFilter, TransactionListFilter
from book.serializers import ListCreateBookSerializer, BookBaseSerializer, BorrowBookSerializer, \
    BorrowBookResponseSerializer, TransactionDetailListSerializer, TransactionListSerializer, RenewSerializer, \
    ReturnSerializer

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
            book = Book.objects.filter(id=int(book_id)).first()

            if not book.is_available:
                raise BookOutOfStock()

            book_already_borrowed = TransactionDetail.objects.filter(
                book=book,
                fk_transaction__fk_user_id=user_id,
                is_returned=False
            ).exists()

            if book_already_borrowed:
                raise BookAlreadyBorrowed

            transaction_detail = TransactionDetail.objects.create(
                book=book,
                fk_transaction=transaction,
                return_deadline=return_deadline
            )

            transaction_borrow_dict["details"].append(transaction_detail)

        serializer = BorrowBookResponseSerializer(transaction_borrow_dict)

        return Response(serializer.data)


class BorrowDetailView(RetrieveAPIView):
    permission_classes = []
    queryset = TransactionDetail.objects.all()
    serializer_class = TransactionDetailListSerializer


class StudentBorrowList(ListAPIView):
    permission_classes = []
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionListFilter


class StudentRenewBorrowView(GenericAPIView):
    permission_classes = []
    queryset = TransactionDetail.objects.all()
    serializer_class = RenewSerializer

    def post(self, request):
        payload = request.data
        transaction_detail_id = payload.get("transaction_detail_id")
        today = datetime.now()
        transaction_detail = self.queryset.filter(id=transaction_detail_id).first()

        if not today.date() <= transaction_detail.return_deadline.date():
            raise RenewedDisallowed()

        if transaction_detail.is_renew:
            raise AlreadyRenewed()

        return_deadline = today + relativedelta(months=+1)
        transaction_detail.return_deadline = return_deadline
        transaction_detail.is_renew = True
        transaction_detail.save()

        serializer = TransactionDetailListSerializer(transaction_detail).data
        return Response(serializer)


class ReturnBookView(GenericAPIView):
    permission_classes = []
    queryset = TransactionDetail.objects.all()
    serializer_class = ReturnSerializer

    def post(self, request):
        payload = request.data
        books = payload.get("books")
        user_id = payload.get("student_id")

        response_list = []
        for book in books:
            transaction_detail = TransactionDetail.objects.filter(
                id=book["transaction_detail_id"],
                fk_transaction__fk_user_id=user_id
            ).first()

            transaction_detail.is_returned = True
            transaction_detail.save()

            response_list.append(transaction_detail)

        serializer = TransactionDetailListSerializer(response_list, many=True).data

        return Response(serializer)
