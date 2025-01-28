ollama serve &
pid=$!
sleep 3
ollama list
echo pulling models
ollama pull llama3.2:1b
ollama pull qwen2.5:1.5b
ollama pull all-minilm
#ollama pull smollm:135m
wait $pid