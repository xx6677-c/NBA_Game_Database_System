"""统一响应格式工具"""
from flask import jsonify
from typing import Any, Dict, Tuple


def success_response(data: Any = None, message: str = 'Success', status_code: int = 200) -> Tuple[Any, int]:
    """
    统一成功响应格式
    
    Args:
        data: 响应数据
        message: 响应消息
        status_code: HTTP状态码
        
    Returns:
        tuple: (响应体, 状态码)
    """
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


def error_response(message: str = 'Error', status_code: int = 400, error_code: str = None) -> Tuple[Any, int]:
    """
    统一错误响应格式
    
    Args:
        message: 错误消息
        status_code: HTTP状态码
        error_code: 业务错误码
        
    Returns:
        tuple: (响应体, 状态码)
    """
    response = {'success': False, 'error': message}
    if error_code:
        response['error_code'] = error_code
    return jsonify(response), status_code
