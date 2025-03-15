from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.core.exceptions import ValidationError


def custom_exception_handler(exc, context):
  response = exception_handler(exc, context)

  # If the response is already handled by DRF, we just enhance it
  if response is not None:
    error_data = {
      'error': True,
      'message': response.data('detail', str(response.data)),
      'code': response.status_code
    }
    response.data = error_data

    return response
  
  # Handle Data integrity
  if isinstance(exc, IntegrityError):
    error_data = {
      'error': True,
      'message': 'Data Integrity Error: Duplicate Entry or Constraint Violation',
      'code': status.HTTP_400_BAD_REQUEST
    }
    return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
  
  # Handle Django Data validation errors
  if isinstance(exc, ValidationError):
    error_data = {
      'error': True,
      'message': str(exc),
      'code': status.HTTP_400_BAD_REQUEST
    }
    return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


  # If unexpected error, return genric error message
  error_data = {
    'error': True,
    'message': 'An unexpected error occurred. Please try again later.',
    'code': status.HTTP_500_INTERNAL_SERVER_ERROR
  }

  return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)