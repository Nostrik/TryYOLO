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

# def main(args):
#     print()
#     # path  = input('path: ').replace('\r','')
#     path = 'C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input'

#     command = ["docker", "run", "-it", "-v", f"{path}:/app/files", "--gpus", "all","dockworker", "-p",f"{path}"]
#     command_without_gpu = ["docker", "run", "-it", "-v", f"{path}:/app/files", "dockworker", "-p", f"{path}"]
    
#     if args.no_gpu:
#         exec_command = command_without_gpu
#     else:
#         exec_command = command

#     if args.lang:
#         save_language_config(args.lang)
#     else:
#         save_language_config('en')
#     lang_config = configparser.ConfigParser()
#     lang_config.read('config.ini')
#     language = lang_config.get('settings', 'language')
#     exec_command.append('-lang')
#     exec_command.append(f'{language}')

#     if args.verbose:
#         exec_command.append("-v")
#         print(exec_command)
#     return_code = subprocess.call(exec_command)
    


# if __name__ == "__main__":
#     parser = MyParser(
#     prog='Video-Content-Inspector',
#     description='Video inspector runner',
#     )
#     parser.add_argument('-v', dest='verbose', action='store_true', required=False, help='verbose option')
#     parser.add_argument('-n_gpu', dest='no_gpu', action='store_true', required=False, help='no gpu option')
#     parser.add_argument('-lang', choices=["en", "ru"], required=False, help='language(en, ru)')
#     args = parser.parse_args()
#     main(args)


def build_docker_command(path, use_gpu, language, verbose):
    base_command = ["docker", "run", "-it", "-v", f"{path}:/app/files"]
    if use_gpu:
        base_command.extend(["--gpus", "all"])
    base_command.append("dockworker")
    base_command.extend(["-p", f"{path}", "-lang", f"{language}"])
    if verbose:
        base_command.append('-v')
    return base_command


def execute_command(command, verbose):
    if verbose:
        print(command)
    return_code = subprocess.call(command)


def main(args):
    path = 'C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input'
    # path  = input('path: ').replace('\r','')
    if args.lang:
        save_language_config(args.lang)
    else:
        save_language_config('en')
    lang_config = configparser.ConfigParser()
    lang_config.read('config.ini')
    language = lang_config.get('settings', 'language')

    docker_command = build_docker_command(path, not args.no_gpu, language, args.verbose)
    execute_command(docker_command, args.verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Video-Content-Inspector', description='Video inspector runner')
    parser.add_argument('-v', dest='verbose', action='store_true', required=False, help='verbose option')
    parser.add_argument('-no_gpu', dest='no_gpu', action='store_true', required=False, help='no gpu option')
    parser.add_argument('-lang', choices=["en", "ru"], required=False, help='language(en, ru)')
    args = parser.parse_args()
    main(args)
