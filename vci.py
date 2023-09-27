import argparse
import sys
import docker
from loguru import logger
from docker.errors import DockerException

docker_client = docker.from_env()
CONTAINER_NAME = "hello world"


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def show_containers():
    print("Show docker images..")
    docker_client.images.list()


def run_container(name_cont):
    print(f"Start docker container ... {name_cont}")
    docker_client.containers.run(name_cont)


def main(args):
    logger.debug(args)
    if args.list_containers==True:
        docker_client.containers.list()
    else:
        run_container(CONTAINER_NAME)



if __name__ == "__main__":
    parser = MyParser(
        prog="Custom Docker App",
        description="custom app for flexible use docker engine"
    )
    parser.add_argument('-l', dest='list_containers', required=False, help='Show all docker images', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    try:
        main(args)
    except DockerException as error:
        print(error)
