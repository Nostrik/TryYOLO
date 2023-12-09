docker image build -t dockworker .

docker container run -i -t -v .\input:/app/files -v .\output:/app/runs/detect/predict --rm cli-util-dockworker -t ad1.mkv -w cigar.pt -c -s

docker image rm cli-util-dockworker


docker-compose run --service-ports vci

docker run -it -v C:\Users\Maxim\tv-21-app\my-tv21-app\input:/app/files --gpus all dockworker

docker save -o dockworker.tar dockworker

docker load -i dockworker.tar