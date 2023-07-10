from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "12J3RHRR744"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Nyandira_20@localhost:3306/phonebook'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True

    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = ""
    app.config['MAIL_PASSWORD'] = ""
    from .models import User, Contact

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    # Import and register blueprints
    from .views import views
    app.register_blueprint(views)

    from .auth import auth
    app.register_blueprint(auth)

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('views.landing_page'))

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Error handling views
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app

