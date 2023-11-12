import sys
import argparse
import subprocess

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def main(args):
    # path  = input('path: ').replace('\r','')
    path = 'C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input'

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
    if args.verbose:
        command.append("-v")
        print(command)
    return_code = subprocess.call(command)


if __name__ == "__main__":
    parser = MyParser(
    prog='Video-Content-Inspector',
    description='Video inspector runner',
    )
    parser.add_argument('-v', dest='verbose', action='store_true', required=False, help='verbose option')
    args = parser.parse_args()
    main(args)
