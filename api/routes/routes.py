from starlette.routing import Route
from api.controllers import containers, images

api_routes = [
    # Route("/containers", recommendations.get_recommendations, name="get_recommendations", methods=['POST']),
    Route('/images', images.get_all, name="get_all", methods=["GET"]),    
]