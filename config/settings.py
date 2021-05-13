import os
import docker
from starlette.config import Config

# Config will be read from environment variables and/or ".env" files.
__config = Config(".env")

DOCKER_HOST_IP = os.getenv("DOCKER_HOST_IP") if os.getenv("DOCKER_HOST_IP") != None else __config('DOCKER_HOST_IP', cast=str, default="192.168.0.178")
DOCKER_HOST_PORT = os.getenv("DOCKER_HOST_PORT") if os.getenv("DOCKER_HOST_PORT") != None else __config('DOCKER_HOST_PORT', cast=str, default="2375")
DOCKER_CLIENT = docker.DockerClient(base_url="http://{}:{}".format(DOCKER_HOST_IP, DOCKER_HOST_PORT))