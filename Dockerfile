FROM ultralytics/ultralytics:latest-python
# FROM python:latest
LABEL maintainer="max"
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN mkdir files

COPY app.py /app/
COPY worker.py /app/
COPY frame2timecode.py /app/
COPY fndBack.py /app/
COPY check_torch.py /app/

RUN apt-get update --fix-missing --no-install-recommends
RUN apt-get install -y --no-install-recommends ffmpeg
RUN pip install colorama --no-cache-dir
RUN pip install loguru --no-cache-dir

RUN apt-get -y install curl

# RUN distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
# RUN curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
# RUN curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

RUN apt-get install -y nvidia-container-toolkit

RUN rm -rf /var/lib/apt/lists/* 

ENTRYPOINT [ "python", "app.py" ]
# ENTRYPOINT [ "python ", "check_torch.py" ]