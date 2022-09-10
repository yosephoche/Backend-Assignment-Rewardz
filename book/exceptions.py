from rest_framework import status
from rest_framework.exceptions import APIException


class BookOutOfStock(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "All book already borrowed"
    }


class MaxBorrowedReach(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "This User have reach maximum borrow per user"
    }