import os
from django.urls import path, include
from book import views

urlpatterns = [
    path("book/", views.BookListView.as_view(), name="BookListView"),
    path("student/borrow-list", views.StudentBorrowList.as_view()),
    path("student/borrow-renew", views.StudentRenewBorrowView.as_view()),
    path("borrow/", views.BorrowView.as_view(), name="BorrowBookView"),
    # path("borrow-list", views.BorrowView.as_view(), name="BorrowBookView"),
    # path("borrow/detail/<int:pk>", views.BorrowView.as_view(), name="BorrowBookView"),
    # path("return-book", views.ReturnBookView.as_view(), name="ReturnBookView"),
]
