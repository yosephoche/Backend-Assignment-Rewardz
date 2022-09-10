from django.db.models import Manager, Count


class UserBookManager(Manager):
    def get_total_borrowed_book(self, user_id) -> int:
        from book.models import TransactionDetail, Transaction
        user = self.filter(id=user_id).first()

        transaction_detail = TransactionDetail.objects.filter(
            fk_transaction__trx_type=Transaction.TRX_TYPE_BORROWED,
            fk_transaction__fk_user=user,
            is_returned=False
        ).annotate(total=Count('book')).values("total").first()

        return transaction_detail['total']
