from rest_framework import serializers

from book.models import Book, TransactionDetail


class BookBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ListCreateBookSerializer(BookBaseSerializer):
    returned_at = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    def get_is_available(self, obj: Book):
        return obj.qty > 0

    def get_returned_at(self, obj: Book):
        if obj.qty > 0:
            return None

        transaction_detail = TransactionDetail.objects.filter(book=obj).order_by("-created_at").first()
        print(transaction_detail)
        return transaction_detail.return_deadline


