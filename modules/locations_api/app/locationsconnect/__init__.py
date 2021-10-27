from app.locationsconnect.models import Location, Person  # noqa
from app.locationsconnect.schemas import LocationSchema  # noqa


def register_routes(api, app, root="api"):
    from app.locationsconnect.controllers import api as locationsapi

    api.add_namespace(locationsapi, path=f"/{root}")
