import subprocess

def main():
    path  = input('path: ').replace('\r','')
    # path = 'C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input'

    command = [
    "docker",
    "run",
    "-it",
    "-v",
    f"{path}:/app/files",
    "--gpus",
    "all",
    "dockworker",
    "-p",
    f"{path}",
    ]
    # print(command)
    return_code = subprocess.call(command)


if __name__ == "__main__":
    main()
