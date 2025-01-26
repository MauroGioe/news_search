import streamlit as st
import subprocess
import sys
import ollama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def scrape_and_save():
    subprocess.run([f"{sys.executable}", "app/web_scraper.py"])


def answer_the_question(question, model, num_doc_to_retrieve, context_window = 20000):
    retrieved_doc = vectordb.similarity_search(question, k = num_doc_to_retrieve)
    #retrieved_doc = retriever.invoke(question)
    print(retrieved_doc)
    context = " ".join(doc.page_content for doc in retrieved_doc)
    response = ollama.chat(model= model, messages=[
      {
        'role': 'user',
        'content': f'''Answer the question according to the context given only if question and context are related:
                       Question: {question}.
                       Context: {context}
                        ''',
      },
    ],  options={"temperature":0, "num_ctx":context_window})
    st.session_state['answer'] = response["message"]["content"]


if 'question' not in st.session_state:
    st.session_state['question'] = ''

if 'answer' not in st.session_state:
    st.session_state['answer'] = ''
if 'num_doc_to_retrieve' not in st.session_state:
    st.session_state['num_doc_to_retrieve'] = "5"

st.button("Scrape video game news", on_click = scrape_and_save)

local_embeddings = OllamaEmbeddings(model = "all-minilm")
vectordb = Chroma(persist_directory = "/dbfs/ChromaDB", embedding_function=local_embeddings, collection_name = "game_news")

st.text_input("What's the maximum number of news you want to hear about?", key="num_doc_to_retrieve")
answer = st.text_input("Ask a video game news related question", key="question", on_change = answer_the_question,
              args = (st.session_state.question, "smollm:135m",  int(st.session_state.num_doc_to_retrieve)))

st.write(st.session_state['answer'])

#st.write(vectordb.get())
#vectordb.delete_collection()