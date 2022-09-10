import os
from django.urls import path, include
from book import views

urlpatterns = [
    path("book/", views.BookListView.as_view(), name="BookListView"),
    path("borrow/", views.BorrowView.as_view(), name="BorrowBookView"),
    # path("return/", views.ReturnBookView.as_view(), name="ReturnBookView"),
]
