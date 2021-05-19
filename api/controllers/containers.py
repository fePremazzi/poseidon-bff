import docker
from starlette.responses import JSONResponse
from config import settings
import docker

DOCKER_CLIENT = docker.DockerClient(base_url="http://{}:{}".format(settings.DOCKER_HOST_IP, settings.DOCKER_HOST_PORT))


def get_by_id(request):
    container_id = request.path_params['container_id']
    output = []

    try:
        container = DOCKER_CLIENT.containers.get(container_id)
    except Exception as e :
        print("Error geting container {0} ".format(e))
        return JSONResponse(output, status_code=404)

    output.append(
        {
            "ShortId": container.attrs["Config"]["Hostname"],
            "Image": container.attrs["Config"]["Image"],
            "Name": container.attrs["Name"][1:],
            "CreatedAt": container.attrs["Created"].split(".")[0],
            "State": container.attrs["State"],
            "Ports": container.attrs["NetworkSettings"]["Ports"],
            "NetworkPorts": container.attrs["NetworkSettings"]["Ports"]
        }
    )
    
    return JSONResponse(output, status_code=200)

def get_all(request):
    containers = None
    output = []

    try:
        containers = DOCKER_CLIENT.containers.list()
    except Exception as e :
        print("Error listing all containers {0} ".format(e))
        return JSONResponse(output, status_code=200)

    for container in containers:
        output.append(
            {
                "ShortId": container.attrs["Config"]["Hostname"],
                "Image": container.attrs["Config"]["Image"],
                "Name": container.attrs["Name"][1:],
                "CreatedAt": container.attrs["Created"].split(".")[0],
                "State": container.attrs["State"],
                "Ports": container.attrs["HostConfig"]["PortBindings"],
                "Env": container.attrs["Config"]["Env"],
                "NetworkPorts": container.attrs["NetworkSettings"]["Ports"]
            }
        )
    
    return JSONResponse(output, status_code=200)

async def run(request):

    output = []
    container = None
    container_image = None
    try:
        #input_data with keys: name, tag
        input_data = await request.json() 
        container_image = input_data["image"]       
    except:
        print("Bad request")
        return JSONResponse({"Error": "Bad request - missing \"image\" on body"}, status_code=400)
    
    container_name = input_data["name"] if 'name' in input_data else None
    container_port = input_data["port"] if 'port' in input_data else None
    container_env = input_data["env"] if 'env' in input_data else None
    if container_port != None:
        external_port, internal_port = container_port.split(":")

    try:
        container = DOCKER_CLIENT.containers.run(image=container_image, 
                                                    detach=True, 
                                                    name=container_name, 
                                                    ports={'{0}/tcp'.format(internal_port):external_port} if container_port != None else None, 
                                                    environment=container_env)
    except Exception as e:
        print("Error creating image {0} . Exception: {1}".format(container_image, e))
        return JSONResponse({"Error": "Error not known: {0}".format(e.args[0].response.content)}, status_code=500)   
    print(container.attrs)
    if container != None:
        output.append(
            {
                "ShortId": container.attrs["Config"]["Hostname"],
                "Image": container.attrs["Config"]["Image"],
                "Name": container.attrs["Name"][1:],
                "CreatedAt": container.attrs["Created"].split(".")[0],
                "State": container.attrs["State"],
                "Ports": container.attrs["HostConfig"]["PortBindings"],
                "Env": container.attrs["Config"]["Env"],
                "NetworkPorts": container.attrs["NetworkSettings"]["Ports"]
            }
        )

    return JSONResponse(output, status_code=200)

def delete_by_id(request):
    container_id = request.path_params['container_id']
    try:
        DOCKER_CLIENT.containers.get(container_id).kill()
    except Exception as e :
        print("Error deleting container {0} . Exception: {1}".format(container_id, e))
        if "No such container:" in str(e.args[0].response.content):
            return JSONResponse({"Error":"No such container as {0}".format(container_id)}, status_code=404)  
        else:
            return JSONResponse({"Error": "Error not known: {0}".format(e.args[0].response.content)}, status_code=500)          
    
    DOCKER_CLIENT.containers.prune()

    return JSONResponse(status_code=204)

def delete_all(request):
    containers = DOCKER_CLIENT.containers.list()
    output = []
    for container in containers:
        container_id = container.attrs["Config"]["Hostname"]
        print("Deleting container: {0}".format(container_id))
        DOCKER_CLIENT.containers.get(container_id).kill()
        output.append(container.attrs["Name"][1:])

    DOCKER_CLIENT.containers.prune()

    return JSONResponse({"Deleted":output}, status_code=200)