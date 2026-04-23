from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['success'] = False

        if response.status_code == 401:
            response.data['message'] = '未授权，请登录'
        elif response.status_code == 403:
            response.data['message'] = '无权限访问'
        elif response.status_code == 404:
            response.data['message'] = '资源不存在'
        elif response.status_code == 400:
            response.data['message'] = '请求参数错误'
        elif response.status_code >= 500:
            response.data['message'] = '服务器内部错误'
            logger.error(f"Server Error: {exc}", exc_info=True)
    else:
        response = Response({
            'success': False,
            'message': '服务器内部错误',
            'status_code': 500
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)

    return response
