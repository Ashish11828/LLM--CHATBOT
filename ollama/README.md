Ollama works by running a model on a server. The server can be accessed locally or
remotely.

Run the server with the start-ollama-server.sh script. The script assumes you have the
ollama Docker image.
To run a model locally...
```
docker exec -it ollama ollama run llama3
```
This takes the "ollama" container and runs `ollama run llama3` in it.
You can use another model in place of "llama3".
