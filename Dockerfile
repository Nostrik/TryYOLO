FROM ultralytics/ultralytics:latest-python
# FROM python:latest
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

RUN apt-get update --fix-missing --no-install-recommends
RUN apt-get install -y --no-install-recommends ffmpeg
RUN pip install colorama --no-cache-dir
RUN pip install loguru --no-cache-dir

# RUN pip install ultralytics
# RUN pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/torch_stable.html
# RUN pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-compiler-10-2 \
    cuda-libraries-dev-10-2 \
    cuda-nvcc-10-2 \
    libcudnn7=7.6.5.32-1+cuda10.2 \
    libcudnn7-dev=7.6.5.32-1+cuda10.2

RUN rm -rf /var/lib/apt/lists/* 

ENTRYPOINT [ "python", "app.py" ]
# ENTRYPOINT [ "python ", "check_torch.py" ]