from functools import wraps

from flask import request, current_app, jsonify
import jwt

from .models import User
from .libs.error_code import TokenInvalidError, TokenExpiredError, UserNotExistError


def login_required(func):
    @wraps(func)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        current_app.logger.debug(f'auth headers: {auth_headers}')

        if len(auth_headers) != 2:
            raise TokenInvalidError

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(username=data['sub']).first()
            if not user:
                raise UserNotExistError
            return func(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError
        except jwt.InvalidTokenError:
            raise TokenInvalidError

    return _verify
