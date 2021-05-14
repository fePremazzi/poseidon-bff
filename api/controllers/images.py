from docker import client
from starlette.responses import JSONResponse
from config import settings
import docker
from requests import exceptions

DOCKER_CLIENT = docker.DockerClient(base_url="http://{}:{}".format(settings.DOCKER_HOST_IP, settings.DOCKER_HOST_PORT))


def get_by_id(request):
    image_id = request.path_params['image_id']
    output = []

    try:
        image = DOCKER_CLIENT.images.get(image_id)
    except Exception as e :
        print("Error geting image {0} ".format(e))
        return JSONResponse(output, status_code=200)


    name, tag = image.attrs["RepoTags"][0].split(":")
    output.append(
        {
            "shortId": image.short_id.split(":")[1],
            "tag": tag,
            "name": name,
            "createdAt": image.attrs["Created"].split(".")[0]
        }
    )
    
    return JSONResponse(output, status_code=200)

def get_all(request):
    images = None
    output = []

    try:
        images = DOCKER_CLIENT.images.list()
    except Exception as e :
        print("Error listing all images {0} ".format(e))
        return JSONResponse(output, status_code=200)

    for image in images:
        name, tag = image.attrs["RepoTags"][0].split(":")
        output.append(
            {
                "shortId": image.short_id.split(":")[1],
                "tag": tag,
                "name": name,
                "createdAt": image.attrs["Created"].split(".")[0]
            }
        )
    
    return JSONResponse(output, status_code=200)

def delete_by_id(request):
    image_id = request.path_params['image_id']
    try:
        DOCKER_CLIENT.images.remove(image_id)
    except Exception as e :
        print("Error deleting image {0} . Exception: {1}".format(image_id, e))
        if "No such image:" in str(e.args[0].response.content):
            return JSONResponse({"error":"No such images as {0}".format(image_id)}, status_code=404)  
        else:
            return JSONResponse({"error": "Error not known: {0}".format(e.args[0].response.content)}, status_code=500)          
    
    return JSONResponse(status_code=204)

def delete_all(request):
    images = DOCKER_CLIENT.images.list()
    output = []
    for image in images:
        name_tag = image.attrs["RepoTags"][0]
        print("Deleting image: {0}".format(name_tag))
        DOCKER_CLIENT.images.remove(image.short_id.split(":")[1])
        output.append(name_tag)

    return JSONResponse({"deleted":output}, status_code=200)
        