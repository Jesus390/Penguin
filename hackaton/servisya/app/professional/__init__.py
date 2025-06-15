from flask import Blueprint

professional_bp = Blueprint('professional', __name__, template_folder='templates')

from app.professional import routes