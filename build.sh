if [ x = x$DOCKER_USER ]; then
	echo "The variable $DOCKER_USER is not set. Try: export DOCKER_USER=<your-docker-id>"
	exit 1
fi

docker build -t $DOCKER_USER/edge-anki-objectdetection .
docker push $DOCKER_USER/edge-anki-objectdetection
