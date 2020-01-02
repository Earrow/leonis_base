from flask import Blueprint

department = Blueprint('department', __name__)

from . import views
