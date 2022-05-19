#!/bin/sh
id=$(docker ps -aqf "name=github-pages")
# echo $id
docker container stop $id