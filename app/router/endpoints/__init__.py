def make_response(status: str, status_code: int, message: str, **kwargs):
    return {'status': status, 'status_code': status_code, 'message': message, **kwargs}
