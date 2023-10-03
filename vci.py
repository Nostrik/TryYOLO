import argparse
import sys
import docker
import subprocess
from loguru import logger
from docker.errors import DockerException

docker_client = docker.from_env()
CONTAINER_NAME = "hello world"
DOCKER_COMPOSE_FILE = ''


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def run_docker_compose():
    try:
        # Путь к файлу docker-compose.yml
        compose_file_path = DOCKER_COMPOSE_FILE

        # Команда для запуска docker-compose
        command = ['docker-compose', 'run', '--service-ports', 'vci']

        # Запуск команды в терминале
        subprocess.run(command, check=True)

        print("Docker-compose приложение успешно запущено!")
    except subprocess.CalledProcessError as e:
        print("Ошибка при запуске docker-compose приложения:", e)


def main(args):
    run_docker_compose()


if __name__ == "__main__":
    parser = MyParser(
        prog="Custom Docker App",
        description="custom app for flexible use docker engine"
    )
    parser.add_argument('-l', dest='list_containers', required=False, help='Show all docker images', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    main(args)
