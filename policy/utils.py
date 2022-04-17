"""
This file is used as common utility functionality.
"""
from utilities import messages
from rest_framework import status
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        customized_response = dict()
        customized_response['error'] = []

        for key, value in response.data.items():
            error = key
            customized_response['status_code'] = response.status_code
            customized_response['error'] = error
            customized_response['data'] = None
            customized_response['message'] = value

        response.data = customized_response

    return response


class ResponseInfo(object):
    """
    Class for setting how API should send response.
    """

    def __init__(self, user=None, **args):
        self.response = {
            "status_code": args.get('status', 200),
            "error": args.get('error', None),
            "data": args.get('data', []),
            "message": args.get('message', 'Success')
        }


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "status_code": status.HTTP_200_OK,
            "error": None,
            "data": {
                'links': {
                    'total_pages': self.page.paginator.num_pages,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'count': self.page.paginator.count,
                'results': data
            },
            "message": "Success"
        })
