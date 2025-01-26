#!/usr/bin/zsh

# grep exits with error code if there are no matches
docker container ls -a -f "name=ollama" | grep -iq "ollama"

# check if last status code is error
if [ $? != 0 ]; then
    docker run -d --gpus=all -v ollama:/root/.ollama --network cb24 -p 11434:11434 --name ollama ollama/ollama
else
    docker container start ollama
fi
