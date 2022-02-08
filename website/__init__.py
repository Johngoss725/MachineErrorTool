
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path,getcwd
import os
import json
from flask_login import LoginManager

#from website.auth import login
#from website.models import manlog


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY']="The secret key "
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)



    from .views import views 
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Note, User, manlog, Userlog

    create_database(app)

    login_manager = LoginManager()
    # This is our redirect
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app = app)
        print("**********************************Created Database*******************")

