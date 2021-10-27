from app.personsconnect.models import Person  # noqa
from app.personsconnect.schemas import PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.personsconnect.controllers import api as personsapi

    api.add_namespace(personsapi, path=f"/{root}")
