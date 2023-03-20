docker rm -f pyChat
docker build -t pychat .
docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)