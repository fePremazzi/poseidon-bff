from starlette.responses import JSONResponse
from config import settings
import docker

DOCKER_CLIENT = docker.DockerClient(base_url="http://{}:{}".format(settings.DOCKER_HOST_IP, settings.DOCKER_HOST_PORT))


def get_all(request):
    images = None
    try:
        images = DOCKER_CLIENT.images.list()
    except Exception as e :
        print(e)

    output = []
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
