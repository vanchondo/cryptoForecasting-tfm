#!/bin/bash
IMAGE=cryptoforecasting-tfm

echo '#### Creating image....'
docker image build -t $IMAGE:latest .

echo '#### Uploading image to jfrog...'
docker tag $IMAGE vanchondo.jfrog.io/tfm/$IMAGE
docker push vanchondo.jfrog.io/tfm/$IMAGE

if [ "$(docker ps -q -f name=$IMAGE)" ]; then
  echo '#### Stopping previous container - '$IMAGE'...'
  docker stop $IMAGE
fi
if [ "$(docker ps -aq -f status=exited -f name=$IMAGE)" ]; then
  echo '#### Removing previous container - '$IMAGE'...'
  docker rm $IMAGE
fi

echo '#### Creating new container - '$IMAGE'...'
docker run --name $IMAGE -d --restart unless-stopped -p6060:6060 $IMAGE:latest

#echo '#### Attaching stdout...'
#docker attach $IMAGE