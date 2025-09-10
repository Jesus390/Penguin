from flask import Flask
from config import Config
from app.extensions import db, login_manager
from app.models.user import User

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # --- LoginManager ---
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Ruta del login si el usuario no está autenticado

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # Registrar blueprints
    from app.auth import auth_bp
    from app.main import main_bp
    from app.professional import professional_bp

    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(professional_bp, url_prefix='/professional')

    return app
