from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import threading
from logging.config import dictConfig
from urllib.parse import quote_plus
import yaml

# Load YAML file into python config object
with open('config.yaml', 'rt') as f:
    yamlconfig = yaml.safe_load(f.read())

dictConfig(yamlconfig['logging-config'])

db = SQLAlchemy(session_options={"expire_on_commit": False})
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = yamlconfig['database']['url'] % quote_plus(yamlconfig['database']['password'])
migrate = Migrate(app, db)
db.init_app(app)

from models import bp as models_bp
app.register_blueprint(models_bp)

from api import bp as api_bp
app.register_blueprint(api_bp)

from repository import bp as repository_bp
app.register_blueprint(repository_bp)

def create_app():
    logging.info('Creating new thread for starting gRPC server...')
    threading.Thread(target=start_grpc_server, daemon=True).start()

    logging.info('Starting main Flask server...')
    return app

with app.app_context():
    db.create_all()
    
def start_grpc_server():
    '''
    Start gRPC server as part of startup logic
    '''
    import grpclib
    import grpclib.grpcserver

    grpclib.grpcserver.serve()


@app.cli.command("manual-grpc")
def manual_start_grpc_server():
    import grpclib
    import grpclib.grpcserver

    logging.info(f'Executing manual gRPC server cli command...')
    grpclib.grpcserver.serve()
