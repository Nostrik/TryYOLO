import sys
import argparse
import subprocess
import configparser

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def save_language_config(language):
    config = configparser.ConfigParser()
    config['settings'] = {'language': language}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def main(args):
    print()
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
    command_without_gpu = [
    "docker",
    "run",
    "-it",
    "-v",
    f"{path}:/app/files",
    "dockworker",
    "-p",
    f"{path}",
    ]
    if args.lang:
        save_language_config(args.lang)
    lang_config = configparser.ConfigParser()
    lang_config.read('config.ini')
    language = lang_config.get('settings', 'language')
    
    if args.no_gpu:
        exec_command = command_without_gpu
    else:
        exec_command = command
    if args.verbose:
        exec_command.append("-v")
        print(exec_command)
    return_code = subprocess.call(exec_command)
    


if __name__ == "__main__":
    parser = MyParser(
    prog='Video-Content-Inspector',
    description='Video inspector runner',
    )
    parser.add_argument('-v', dest='verbose', action='store_true', required=False, help='verbose option')
    parser.add_argument('-n_gpu', dest='no_gpu', action='store_true', required=False, help='no gpu option')
    parser.add_argument('-lang', choices=["en", "ru"], required=False, help='language(en, ru)')
    args = parser.parse_args()
    main(args)
