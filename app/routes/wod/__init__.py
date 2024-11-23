from flask import Blueprint

wod_bp = Blueprint('wod_bp', __name__)

from . import routes
