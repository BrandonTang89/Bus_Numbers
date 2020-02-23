docker build -t custom_vision ./custom_vision_docker
docker run -p 127.0.0.1:80:80 -d custom_vision
sleep 3
