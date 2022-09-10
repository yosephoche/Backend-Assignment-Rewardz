from django_filters.rest_framework import FilterSet, filters

from book.models import Book


class BookListFilter(FilterSet):
    search_by_title = filters.CharFilter(field_name="title", method='search')
    search_by_author = filters.CharFilter(field_name="author", method='search')

    class Meta:
        model = Book
        fields = ["search_by_title", "search_by_author"]

    def search(self, queryset, field, value):
        lookup = "%s__contains" % field
        return queryset.filter(**{lookup: value})
