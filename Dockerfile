FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04
LABEL maintainer="max"

#install python
RUN apt update
RUN apt-get install -y python3 python3-pip

#create workdir
WORKDIR /app
RUN mkdir files

#install app
COPY app.py /app/
COPY worker.py /app/
COPY frame2timecode.py /app/
COPY fndBack.py /app/
COPY check_torch.py /app/

#install requirements
RUN pip install --upgrade pip
RUN apt-get update --fix-missing --no-install-recommends
RUN apt-get install -y --no-install-recommends ffmpeg
RUN pip install colorama --no-cache-dir
RUN pip install loguru --no-cache-dir
RUN pip install ultralytics

#install pytorch
RUN pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

RUN rm -rf /var/lib/apt/lists/* 

ENTRYPOINT [ "python3", "app.py" ]
# ENTRYPOINT [ "python ", "check_torch.py" ]
