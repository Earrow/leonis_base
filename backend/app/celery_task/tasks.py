from .. import celery
from ..models import User


@celery.task
def add_together(a, b):
    return a + b


@celery.task
def get_users():
    users = User.query.all()
    print([u.username for u in users])
    return str([u.username for u in users])
