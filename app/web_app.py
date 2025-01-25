import ollama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


def answer_the_question(question, context, context_window = 20000):
    response = ollama.chat(model='llama3.2:latest', messages=[
      {
        'role': 'user',
        'content': f'''Answer the question according to the context given very briefly:
                       Question: {question}.
                       Context: {context}
                        ''',
      },
    ],  options={"temperature":0, "num_ctx":context_window})
    return response["message"]["content"]

local_embeddings = OllamaEmbeddings(model = "all-minilm")
vectordb = Chroma(embedding_function=local_embeddings, collection_name = "game_news")
question="tell me news about the switch 2"
num_doc_to_retrieve = 2
retriever = vectordb.as_retriever(search_type = "similarity", search_kwargs= {"k":num_doc_to_retrieve})
retrieved_doc = retriever.invoke(question)
context = " ".join(doc.page_content for doc in retrieved_doc)
answer_the_question(question, context)