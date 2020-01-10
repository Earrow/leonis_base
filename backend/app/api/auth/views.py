from datetime import datetime, timedelta

import jwt
from flask import current_app, request

from . import auth
from ... import db
from ...models import User, Administrator
from ...forms.user_form import UserForm
from ...libs.error_code import OK, CredentialsError, TokenExpiredError, TokenInvalidError, UserNotExistError


@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    form = UserForm(data).validate()

    username = form.username.data
    password = form.password.data
    name = form.name.data

    user = User(username=username, password=password, name=name)
    db.session.add(user)
    db.session.commit()
    current_app.logger.info(f'新注册用户: {username}')

    return OK(code=201)


@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.authenticate(username, password)

    if not user:
        current_app.logger.warning(f'{username} 登录失败')
        raise CredentialsError

    token = jwt.encode({
        'sub': username,  # 内容
        'iat': datetime.utcnow(),  # 创建时间
        'exp': datetime.utcnow() + timedelta(minutes=current_app.config['TOKEN_EXPIRE_TIME'])  # 过期时间
    },
        current_app.config['SECRET_KEY'])
    current_app.logger.info(f'{username} 登录')

    return OK(token=token.decode('utf-8'))


@auth.route('/get-user-info', methods=['POST'])
def get_user_info():
    token = request.json.get('token')

    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        user = User.query.filter_by(username=data['sub']).first()
        if user:
            return OK(user={
                'username': user.username,
                'active_project': {
                    'id': user.active_project.id,
                    'name': user.active_project.name,
                    'is_master': True if user in user.active_project.masters else False
                } if user.active_project else None,
                'is_admin': Administrator.has(user)
            })
        else:
            return UserNotExistError()
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError
    except jwt.InvalidTokenError:
        raise TokenInvalidError
