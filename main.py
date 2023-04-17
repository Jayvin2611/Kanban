from flask import Flask,render_template,request
from flask import current_app as app
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from application.model import *
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from  datetime import datetime
from application.api import *
import pytz
from flask_cors import CORS
from application.workers import *
from application.tasks import *
from flask_caching import Cache



IST = pytz.timezone('Asia/Kolkata')


from flask.sessions import SecureCookieSessionInterface, SessionMixin


class CustomSessionInterface(SecureCookieSessionInterface):
    def should_set_cookie(self, app: 'Flask', session: SessionMixin) -> bool:
        return False


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.app_context().push()
db.create_all()
api = Api(app)
cors = CORS(app)
app.config['SECRET_KEY'] = 'secret key'
app.config['SECURITY_PASSWORD_HASH'] = 'sha256_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'jayvin'
app.config['SECURITY_REGISTERABLE'] = False
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_UNAUTHORIZED_VIEW'] = None
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config['CELERY_BROKER_URL'] = "redis://127.0.0.1:6379/1"
app.config['CELERY_RESULT_BACKEND'] = "redis://127.0.0.1:6379/2"
app.config['REDIS_URL'] = "redis://localhost:6379"
app.config['CACHE_TYPE'] = "RedisCache"
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['CACHE_REDIS_HOST'] = "localhost"
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 3
user_datastore = SQLAlchemySessionUserDatastore(db.session, User,Role)
security=Security(app, user_datastore)
app.session_interface = CustomSessionInterface()
celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
celery.Task = ContextTask
cache.init_app(app)
app.app_context().push()



api.add_resource(UserApi,'/api/user')
api.add_resource(ListApi,'/api/list','/api/list/<int:id>')
api.add_resource(CardApi,'/api/card','/api/card/<int:id>')
api.add_resource(Export,'/api/export/<int:id>')
api.add_resource(Link,'/api/link')
api.add_resource(ChartDataApi,'/api/chart')
api.add_resource(DragDrop,'/api/dragdrop')

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8080)