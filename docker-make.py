import sys
import subprocess

file_path = './worker.py'

for line in fileinput.input(file_path, inplace=True):
    sys.stdout.write(line.replace(".venv/Scripts/python", "python"))

subprocess.run(["docker", "image", "build", "-t", "cli-util-dockworker", "."], check=True)
subprocess.run(["docker", "container", "run", "-i", "-t", "-v", ".\\input:/app/files", "-v", ".\\output:/app/runs/detect/predict", "--rm", "cli-util-dockworker", "-t", "ad1.mkv", "-w", "cigar.pt", "-c", "-s"], check=True)