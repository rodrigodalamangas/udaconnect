import logging
import json
from datetime import datetime, timedelta
from typing import Dict
from flask import Response
from app import db
from app.locationsconnect.models import Location
from app.locationsconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

from app import g

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("locationsapi")


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Dict:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(
                f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        kafka_data = json.dumps(location).encode('utf-8')
        kafka_producer = g.kafka_producer
        kafka_producer.send('locations', kafka_data)

        return Response(status=202)
