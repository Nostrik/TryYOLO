# FROM ultralytics/ultralytics:latest-python
FROM python:latest
LABEL maintainer="max"
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN mkdir files

COPY app.py /app/
COPY worker.py /app/
COPY detect.py /app/
COPY frame2timecode.py /app/
COPY fndBack.py /app/
COPY check_torch.py /app/

RUN apt-get update --fix-missing
RUN apt-get install -y ffmpeg
RUN pip install colorama
RUN pip install loguru

RUN pip install ultralytics
RUN pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

RUN rm -rf /var/lib/apt/lists/* 

ENTRYPOINT [ "python", "app.py" ]
# ENTRYPOINT [ "python ", "check_torch.py" ]