from flask import Flask, render_template
from routes.student_routes import student_bp
from routes.auth_routes import auth_bp
from config import Config
from flask_wtf.csrf import CSRFProtect
import os
from database import (
    create_courses_table,
    create_student_courses_table,
    create_default_courses
)
from routes.api_routes import api_bp
from flask_jwt_extended import JWTManager

csrf = CSRFProtect()
jwt = JWTManager()

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    csrf.init_app(app)
    jwt.init_app(app)

    create_courses_table()
    create_student_courses_table()
    create_default_courses()


    app.register_blueprint(student_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    csrf.exempt(api_bp)


    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"),404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("500.html"),500

    @app.errorhandler(403)
    def access_error(error):
        return render_template("403.html"),403

    @app.errorhandler(413)
    def large_file_error(error):
        return "File is too large. Maximum size allowed is 2MB.",413

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)         
