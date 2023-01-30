from flask import Flask,session
import mysql.connector

db=mysql.connector.connect(host='localhost',user='root',password='tanmay@mySQL',database='anigle_alt')
cursor=db.cursor()

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='secret'

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    return app