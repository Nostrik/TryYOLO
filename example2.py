import time
from multiprocessing.managers import BaseManager


def get_time():
    return time.time()


if __name__ == "__main__":
    BaseManager.register("get", callable=get_time)
    manager = BaseManager(address=('', 4444), authkey=b'abc')
    server = manager.get_server()
    print("server start")
    server.serve_forever()
