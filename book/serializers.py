from rest_framework import serializers

from authentication.serializers import UserBaseSerializer, UserMinimalSerializer
from book.models import Book, TransactionDetail, Transaction


class BookBaseSerializer(serializers.ModelSerializer):
    returned_at = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    def get_is_available(self, obj: Book):
        return obj.is_available

    def get_returned_at(self, obj: Book):
        return obj.returned_at

    class Meta:
        model = Book
        fields = "__all__"


class ListCreateBookSerializer(BookBaseSerializer):
    pass


class BorrowBookSerializer(serializers.Serializer):
    fk_user_id = serializers.IntegerField()
    trx_type = serializers.CharField()
    books = serializers.ListField()


class TransactionBaseSerializer(serializers.ModelSerializer):
    fk_user = UserMinimalSerializer()

    class Meta:
        model = Transaction
        fields = "__all__"


class TransactionDetailBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = "__all__"


class TransactionDetailListSerializer(TransactionDetailBaseSerializer):
    book = serializers.SerializerMethodField()

    class Meta(TransactionDetailBaseSerializer.Meta):
        fields = ["id", "book", "is_renew", "return_deadline", "created_at", "updated_at"]

    def get_book(self, obj: TransactionDetail):
        books = Book.objects.filter(id=obj.book_id)
        return BookBaseSerializer(books, many=True).data


class TransactionListSerializer(TransactionBaseSerializer):
    details = serializers.SerializerMethodField()

    def get_details(self, obj: Transaction):
        details = TransactionDetail.objects.filter(fk_transaction=obj)
        return TransactionDetailListSerializer(details, many=True).data


class BorrowBookResponseSerializer(serializers.Serializer):
    trx_id = serializers.IntegerField()
    details = serializers.ListField(child=TransactionDetailListSerializer())


class RenewSerializer(serializers.Serializer):
    transaction_detail_id = serializers.IntegerField()
