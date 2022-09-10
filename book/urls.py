import os
from django.urls import path, include
from book import views

urlpatterns = [
    path("book/", views.BookListView.as_view(), name="BookListView"),
    path("student/borrow-list", views.StudentBorrowList.as_view()),
    path("student/borrow-renew", views.StudentRenewBorrowView.as_view()),
    path("borrow/", views.BorrowView.as_view(), name="BorrowBookView"),
    path("borrow/detail/<int:pk>", views.BorrowDetailView.as_view(), name="BorrowBookView"),
    path("return", views.ReturnBookView.as_view()),
]
