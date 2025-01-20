ollama serve &
pid=$!
sleep 3
ollama list
#ollama pull llama3.2:3b
echo pull model
ollama pull smollm:135m
wait $pid