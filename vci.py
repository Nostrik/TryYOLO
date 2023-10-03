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


def main(args):
    path_to_yaml_file = input("Укажите каталог с данными: ").replace('\r','')



if __name__ == "__main__":
    parser = MyParser(
        prog="Custom Docker App",
        description="custom app for flexible use docker engine"
    )
    parser.add_argument('-l', dest='list_containers', required=False, help='Show all docker images', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    main(args)

