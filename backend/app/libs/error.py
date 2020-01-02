from flask import request, json
from werkzeug.exceptions import HTTPException


class APIError(HTTPException):
    code = 500
    msg = '服务器遇到了一个错误'
    error_code = 199999
    kwargs = None

    def __init__(self, code=None, msg=None, error_code=None, **kwargs):
        self.code = code or self.code
        self.msg = msg or self.msg
        self.error_code = error_code or self.error_code
        self.kwargs = kwargs or self.kwargs

        super().__init__(self.msg)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=f'{request.method} {self._get_url_without_params()}'
        )
        if self.kwargs:
            body.update(self.kwargs)

        return json.dumps(body)

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def _get_url_without_params():
        full_path = str(request.full_path)
        return full_path.split('?')[0]
