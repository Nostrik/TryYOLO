import argparse
import sys
import docker
from loguru import logger

docker_client = docker


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    print("Start docker container ...")
    pass


if __name__ == "__main__":
    main()
