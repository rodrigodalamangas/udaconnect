from flask import request
from app.locationsconnect.models import Location
from app.locationsconnect.schemas import LocationSchema
from app.locationsconnect.services import LocationService
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource


api = Namespace("Locations Api", description="Locations Api for UdaConnect.")  # noqa


@api.route("/locations")
class LocationsResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        location: Location = LocationService.create(request.get_json())
        return location


@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
