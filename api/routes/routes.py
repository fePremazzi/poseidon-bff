from starlette.routing import Route
from api.controllers import containers, images

api_routes = [
    # Route("/containers", recommendations.get_recommendations, name="get_recommendations", methods=['POST']),
    Route('/images', images.get_all, name="get_all", methods=["GET"]),
    Route('/images/{image_id:str}', images.delete_by_id, name="delete_by_id", methods=["DELETE"]),
    Route('/images', images.delete_all, name="delete_all", methods=["DELETE"]),    
]