from starlette.routing import Route
from api.controllers import containers, images

routes = [
    # Route("/containers", recommendations.get_recommendations, name="get_recommendations", methods=['POST']),
    # Route('/images', settings.set_limit, name="set_limit", methods=["POST"]),    
]