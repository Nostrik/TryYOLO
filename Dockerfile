FROM ultralytics/ultralytics:latest-python
LABEL maintainer="max"
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN mkdir files

COPY app.py /app/
COPY worker.py /app/
COPY detect.py /app/
COPY frame2timecode.py /app/
COPY fndBack.py /app/

RUN apt-get update --fix-missing
RUN apt-get install -y ffmpeg
RUN pip install colorama
RUN rm -rf /var/lib/apt/lists/* 

ENTRYPOINT [ "python", "app.py" ]