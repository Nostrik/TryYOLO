docker image build -t cli-util-dockworker .

docker container run -i -t -v .\input:/app/files -v .\output:/app/runs/detect/predict --rm cli-util-dockworker -t ad1.mkv -w cigar.pt -c -s

docker image rm cli-util-dockworker


docker run -i -v C:\Users\Maxim\tv-21-app\tv21-app-rep\input:/app/files --rm cli-util-dockworker

docker run -i -v C:\Users\Maxim\tv-21-app\tv21-app-rep\input:/app/files -v C:\Users\Maxim\tv-21-app\tv21-app-rep\output:/app/runs/detect/predict  --rm cli-util-dockworker -c -s

