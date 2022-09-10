from django_filters.rest_framework import FilterSet, filters

from book.models import Book, Transaction


class BookListFilter(FilterSet):
    search_by_title = filters.CharFilter(field_name="title", method='search')
    search_by_author = filters.CharFilter(field_name="author", method='search')

    class Meta:
        model = Book
        fields = ["search_by_title", "search_by_author"]

    def search(self, queryset, field, value):
        lookup = "%s__contains" % field
        return queryset.filter(**{lookup: value})


class TransactionListFilter(FilterSet):
    search_by_user_email = filters.CharFilter(field_name="user", method="search")
    filter_by_user_id = filters.CharFilter(field_name="fk_user_id")
    filter_by_status = filters.CharFilter(field_name="status")

    class Meta:
        model = Transaction
        fields = ["search_by_user_email", "filter_by_user_id", "filter_by_status"]

    def search(self, queryset, field, value):
        return queryset.filter(fk_user__email__icontains=value)

