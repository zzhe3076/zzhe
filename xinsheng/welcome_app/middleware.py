from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework import status
import time
import logging

logger = logging.getLogger(__name__)


class APILogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        return None

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            if request.path.startswith('/api/'):
                logger.info(f"{request.method} {request.path} - {response.status_code} - {duration:.2f}s")
        return response


class APIResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/api/') and not isinstance(response, Response):
            if response.status_code >= 200 and response.status_code < 300:
                return Response({
                    'success': True,
                    'data': response.data,
                }, status=response.status_code)
        return response
