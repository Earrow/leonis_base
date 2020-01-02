from datetime import datetime

from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

department_users = db.Table('department_users',
                            db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                            db.Column('department_id', db.Integer, db.ForeignKey('departments.id')))

department_masters = db.Table('department_masters',
                              db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                              db.Column('department_id', db.Integer, db.ForeignKey('departments.id')))

project_users = db.Table('project_users',
                         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                         db.Column('project_id', db.Integer, db.ForeignKey('projects.id')))

project_masters = db.Table('project_masters',
                           db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                           db.Column('project_id', db.Integer, db.ForeignKey('projects.id')))


class User(db.Model):
    """用户。"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, comment='用户名')
    password_hash = db.Column(db.String(128), comment='哈希密码')
    name = db.Column(db.String(16), default='', comment='姓名')

    administrator = db.relationship('Administrator', back_populates='user', uselist=False,
                                    cascade='all, delete, delete-orphan', doc='是否是管理员')

    departments = db.relationship('Department', secondary=department_users, back_populates='users', lazy='dynamic',
                                  doc='部门')
    master_departments = db.relationship('Department', secondary=department_masters, back_populates='masters',
                                         lazy='dynamic', doc='管理部门')

    projects = db.relationship('Project', secondary=project_users, back_populates='users', lazy='dynamic', doc='项目')
    master_projects = db.relationship('Project', secondary=project_masters, back_populates='masters', lazy='dynamic',
                                      doc='管理项目')

    active_project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), comment='活动项目id')
    active_project = db.relationship('Project', back_populates='active_users', doc='活动用户')

    @property
    def password(self):
        raise AttributeError('不能读取密码明文')

    @password.setter
    def password(self, password):
        """设置password属性时，转而设置password_hash，赋值为密码的哈希值。

        :param password: 密码明文。
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """校验密码。

        :param password: 密码明文。
        :return: 密码正确时返回True，否则返回False。
        """
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, username, password):
        """校验用户名和密码。

        :param username: 用户名
        :param password: 密码
        :return: 用户名存在且密码正确时，返回该用户对象；否则返回None。
        """
        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return None

        return user

    def is_administrator(self):
        """判断用户是否是平台管理员。"""
        return self.administrator

    def to_dict(self):
        return dict(id=self.id, username=self.username, name=self.name)

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'


class Administrator(db.Model):
    """平台管理员。"""
    __tablename__ = 'administrators'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='administrator')

    @classmethod
    def contain(cls, user: User):
        """判断用户是否是平台管理员。

        :param user: 用户对象。
        :return: 若用户对象是平台管理员则返回该用户对象；否则返回None。
        """
        user_id = user.id
        admin = cls.query.filter_by(user_id=user_id).first()
        return admin


class Department(db.Model):
    """部门。"""
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, comment='名称')
    enable = db.Column(db.Boolean, default=True, comment='是否启用')
    is_top = db.Column(db.Boolean, default=True, comment='是否是顶级部门')

    users = db.relationship('User', secondary=department_users, back_populates='departments', lazy='dynamic',
                            doc='用户')
    masters = db.relationship('User', secondary=department_masters, back_populates='master_departments', lazy='dynamic',
                              doc='管理员')

    parent_department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), comment='上级部门id')
    child_departments = db.relationship('Department', backref=backref('parent_department', remote_side=[id]),
                                        lazy='dynamic', doc='下级部门')

    projects = db.relationship('Project', back_populates='department', doc='项目')

    def __repr__(self):
        return f'<Department {self.id}, {self.name}>'


class Project(db.Model):
    """项目。"""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, comment='名称')
    enable = db.Column(db.Boolean, default=True, comment='是否启用')

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), comment='所属部门id')
    department = db.relationship('Department', back_populates='projects')

    users = db.relationship('User', secondary=project_users, back_populates='projects', lazy='dynamic', doc='用户')
    masters = db.relationship('User', secondary=project_masters, back_populates='master_projects', lazy='dynamic',
                              doc='管理用户')

    active_users = db.relationship('User', back_populates='active_project', doc='活动用户')

    def __repr__(self):
        return f'<Project {self.id}, {self.name}>'
