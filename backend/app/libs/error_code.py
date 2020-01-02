from .error import APIError


class OK(APIError):
    code = 200
    msg = 'OK'
    error_code = 0


class ServerError(APIError):
    code = 500
    msg = '服务器遇到了一个错误'
    error_code = 1000


class ParamsError(APIError):
    code = 400
    msg = '参数无效'
    error_code = 1001


# 认证错误
class TokenInvalidError(APIError):
    code = 401
    msg = 'Token无效'
    error_code = 2001


class TokenExpiredError(APIError):
    code = 401
    msg = 'Token过期'
    error_code = 2002


class UserNotExistError(APIError):
    code = 202
    msg = '用户不存在'
    error_code = 2003


class CredentialsError(APIError):
    code = 400
    msg = '用户名或密码错误'
    error_code = 2004
