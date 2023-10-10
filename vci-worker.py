import docker

import docker

# Создание клиента Docker
client = docker.from_env()




if __name__ == "__main__":
    # Запуск контейнера с командой nvidia-smi и использованием GPU
    container = client.containers.run(
    'ultralytics/ultralytics',
    command='nvidia-smi',
    runtime='nvidia',  # Указываем использование NVIDIA Runtime
    detach=True
)

    # Дополнительные действия с контейнером...

    # Удаление контейнера
    container.stop()
    container.remove()
