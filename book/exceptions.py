from rest_framework import status
from rest_framework.exceptions import APIException


class BookOutOfStock(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "All book already borrowed"
    }


class BookAlreadyBorrowed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "Book Already Borrowed, Return it first or you can renew once"
    }


class MaxBorrowedReach(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "This User have reach maximum borrow per user"
    }


class AlreadyRenewed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "This transaction already renewed"
    }


class RenewedDisallowed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "Can't renew outside borrow period"
    }