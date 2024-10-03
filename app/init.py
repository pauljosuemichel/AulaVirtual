from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializar las extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuraciones
    app.config['SECRET_KEY'] = 'tu_clave_secreta'  # Cambia esto por una clave secreta más segura
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:contraseña@localhost/nombre_db'  # Ajusta según tu configuración
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar las extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Cargar las rutas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Inicializar la base de datos
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos

    return app
