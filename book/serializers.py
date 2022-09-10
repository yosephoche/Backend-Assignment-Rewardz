from rest_framework import serializers

from book.models import Book, TransactionDetail


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


class TransactionDetailBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = "__all__"


class TransactionDetailListSerializer(TransactionDetailBaseSerializer):
    books = serializers.ListField(child=BookBaseSerializer())

    class Meta(TransactionDetailBaseSerializer.Meta):
        fields = ["id", "books", "is_renew", "return_deadline", "created_at", "updated_at"]


class BorrowBookResponseSerializer(serializers.Serializer):
    trx_id = serializers.IntegerField()
    details = serializers.ListField(child=TransactionDetailListSerializer())

