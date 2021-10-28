from app.personsconnect.models import Person
from app.personsconnect.schemas import PersonSchema
from app.personsconnect.services import PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, fields
from typing import List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("Persons Api", description="Persons Api for UdaConnect.")  # noqa
# Swagger Model for Person post
modelo = api.model('PersonModel', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'company_name': fields.String,
})


@api.route("/persons")
class PersonsResource(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(modelo)
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person
