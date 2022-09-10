import os
from django.urls import path, include
from book import views

urlpatterns = [
    path("book/", views.BookListView.as_view(), name="BookListView"),
]
