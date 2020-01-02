from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, length, EqualTo
from wtforms import ValidationError

from .base_form import BaseForm
from ..models import User


class UserForm(BaseForm):
    username = StringField(validators=[DataRequired('用户名不能为空')])
    password = PasswordField(validators=[DataRequired('密码不能为空'),
                                         length(min=6, max=18, message='密码长度必须在6-18位之间'),
                                         EqualTo('password_confirm', message='两次输入密码必须一致')])
    password_confirm = PasswordField(validators=[DataRequired('请确认密码')])
    name = StringField()

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('此用户名已注册')
