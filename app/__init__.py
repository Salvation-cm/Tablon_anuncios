from flask import Flask
from flask_login import LoginManager
from app.models.models import db, Usuario

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave_secreta_super_segura'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from app.auth.routes import auth_bp
    from app.anuncios.routes import anuncios_bp
    from app.categorias.routes import categorias_bp
    from app.usuarios.routes import usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(anuncios_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(usuarios_bp)

    with app.app_context():
        db.create_all()

    return app