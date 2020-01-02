from flask_wtf import FlaskForm

from ..libs.error_code import ParamsError


class BaseForm(FlaskForm):
    def __init__(self, data, **kwargs):
        super().__init__(data=data, meta={'csrf': False}, **kwargs)

    def validate(self):
        valid = super().validate()
        if not valid:
            raise ParamsError(msg=self.errors)

        return self
