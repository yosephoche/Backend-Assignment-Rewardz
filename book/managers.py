from django.db.models import Manager


class BookManager(Manager):
    pass


class TransactionDetailManager(Manager):
    def count_borrowed_book(self, book_id):
        return self.filter(book_id=book_id).count()

    def count_borrowed_book_by_student(self, student_id):
        return self.filter(is_returned=False, fk_transaction__fk_user_id=student_id).count()
