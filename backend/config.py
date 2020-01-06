import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    TOKEN_EXPIRE_TIME = 720  # token过期时间，单位：分钟

    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/leonis?charset=utf8mb4'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from flask.logging import default_handler

        logger = logging.getLogger('leonis')
        logger.setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(module)s.%(funcName)s(): %(lineno)d] %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        app.logger.removeHandler(default_handler)
        app.logger.addHandler(stream_handler)
        logger.addHandler(stream_handler)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/leonis?charset=utf8mb4'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from flask.logging import default_handler
        from logging.handlers import RotatingFileHandler

        logger = logging.getLogger('leonis')
        logger.setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(module)s.%(funcName)s(): %(lineno)d] %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(
            'log/leonis.log',
            maxBytes=100 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        app.logger.removeHandler(default_handler)
        app.logger.addHandler(stream_handler)
        app.logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
