from starlette.routing import Route
from api.controllers import containers, images

api_routes = [
    Route('/images', images.get_all, name="get_all", methods=["GET"]),
    Route('/images/{image_id:str}', images.get_by_id, name="get_by_id", methods=["GET"]),
    Route('/images/{image_id:str}', images.delete_by_id, name="delete_by_id", methods=["DELETE"]),
    Route('/images', images.delete_all, name="delete_all", methods=["DELETE"]),    
    Route('/images', images.pull, name="pull", methods=["POST"]),    

    Route('/containers', containers.get_all, name="get_all", methods=["GET"]),
    Route('/containers/{container_id:str}', containers.get_by_id, name="get_by_id", methods=["GET"]),
    Route('/containers/{container_id:str}', containers.delete_by_id, name="delete_by_id", methods=["DELETE"]),
    Route('/containers', containers.delete_all, name="delete_all", methods=["DELETE"]),    
    Route('/containers', containers.run, name="run", methods=["POST"]),
]