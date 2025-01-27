ollama serve &
pid=$!
sleep 3
ollama list
echo pulling models
ollama pull llama3.2:1b
ollama pull all-minilm
#ollama pull smollm:135m
wait $pid