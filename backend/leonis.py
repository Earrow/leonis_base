import os

import click
from flask import request, request_started
from flask.cli import AppGroup
from werkzeug.exceptions import HTTPException

from .app import create_app, db
from .app.models import User, Administrator, Department, Project
from .app.libs.error import APIError
from .app.libs.error_code import ServerError

app = create_app(os.getenv('FLASK_ENV') or 'default')

user_cli = AppGroup('user')


@user_cli.command('add')
@click.argument('username')
def add_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, password=username)
        db.session.add(user)
        db.session.commit()


@user_cli.command('del')
@click.argument('username')
def del_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()


@user_cli.command('add-admin')
@click.argument('username')
def add_admin(username):
    user = User.query.filter_by(username=username).first()
    if user:
        admin = Administrator(user=user)
        db.session.add(admin)
        db.session.commit()


@user_cli.command('del-admin')
@click.argument('username')
def del_admin(username):
    user = User.query.filter_by(username=username).first()
    if user:
        admin = Administrator.query.filter_by(user=user).first()
        db.session.delete(admin)
        db.session.commit()


app.cli.add_command(user_cli)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Administrator=Administrator, Department=Department, Project=Project)


def log_request(sender, **extra):
    sender.logger.info(
        f'{request.method} {request.url}, data: {request.data}, json: {request.json}, files: {request.files}')


request_started.connect(log_request, app)


@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, APIError):
        return e
    elif isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 9000
        return APIError(msg=msg, code=code, error_code=error_code)
    else:
        if not app.config['DEBUG']:
            raise ServerError
        else:
            raise e


@app.route('/test')
def test():
    return '测试页面'
