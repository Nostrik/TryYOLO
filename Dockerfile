FROM ultralytics/ultralytics:latest
LABEL maintainer="max"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

#create workdir
WORKDIR /app
RUN mkdir files

#install app
COPY vci.py /app/
COPY core.py /app/
COPY black_finder.py /app/
COPY frame_temp.py /app/
COPY frame2timecode.py /app/
COPY loader.py /app/
COPY messages.py /app/
COPY models.py /app/

#del temp packets
RUN rm -rf /var/lib/apt/lists/*

#run
ENTRYPOINT [ "python3", "vci.py" ]
