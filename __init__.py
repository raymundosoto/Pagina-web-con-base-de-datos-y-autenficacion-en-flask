from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf import CSRFProtect

mysql = MySQL()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuraciones
    app.config.from_object('flask_app.config.Config')
    
    # Inicializar extensiones
    mysql.init_app(app)
    csrf.init_app(app)
    
    # Registrar las rutas
    with app.app_context():
        from flask_app import routes
        app.register_blueprint(routes.bp)

    return app
