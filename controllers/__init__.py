from flask import Blueprint

file_controller = Blueprint('file', __name__)

from . import file