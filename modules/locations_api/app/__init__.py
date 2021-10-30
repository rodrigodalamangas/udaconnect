import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="Locations API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    @app.before_request
    def before_request():
        # Set up a Kafka producer
        KAFKA_PRODUCER = os.environ["KAFKA_PRODUCER"]
        #KAFKA_PRODUCER = 'localhost:9092'
        producer = KafkaProducer(bootstrap_servers=[KAFKA_PRODUCER])
        # Setting Kafka to g enables us to use this
        # in other parts of our application
        g.kafka_producer = producer

    return app
