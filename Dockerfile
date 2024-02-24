FROM ultralytics/ultralytics:8.1.17
LABEL maintainer="max"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TERM xterm-256color

RUN echo 'export TERM=xterm-256color' >> ~/.bashrc

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

#requirements
RUN pip install --upgrade pip
RUN pip install loguru
RUN pip install termcolor

#install pytorch
RUN pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

#del temp packets
RUN rm -rf /var/lib/apt/lists/*

#run
# RUN poetry shell
ENTRYPOINT [ "python3", "vci.py" ]
