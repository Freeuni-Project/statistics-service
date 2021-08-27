# application/statistics_api/__init__.py
from flask import Blueprint

statistics_api_blueprint = Blueprint('statistics_api', __name__)

from . import routes
