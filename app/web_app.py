import streamlit as st
import subprocess
import sys
import ollama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from ollama import Client
ollama_client = Client(host='http://ollama:11434/')

def scrape_and_save():
    subprocess.run([f"{sys.executable}", "./web_scraper.py"])


def answer_the_question(model, num_doc_to_retrieve, context_window = 20000):
    question = st.session_state.question
    retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": num_doc_to_retrieve, "lambda_mult": 1})
    retrieved_doc = retriever.invoke(question)
    print(retrieved_doc)
    context = " ".join(doc.page_content for doc in retrieved_doc)
    response = ollama_client.chat(model= model, messages=[
      {
        'role': 'user',
        'content': f'''   Context: {context}.
                    Answer the following question according to the context provided.
                    Question: {question}.
                        ''',
      },
    ],  options={"temperature":0, "num_ctx":context_window})
    st.session_state['answer'] = response["message"]["content"]


if 'question' not in st.session_state:
    st.session_state['question'] = ''

if 'answer' not in st.session_state:
    st.session_state['answer'] = ''
if 'num_doc_to_retrieve' not in st.session_state:
    st.session_state['num_doc_to_retrieve'] = "3"

st.button("Scrape video game news", on_click = scrape_and_save)

local_embeddings = OllamaEmbeddings(model = "mxbai-embed-large", base_url = 'http://ollama:11434/')
vectordb = Chroma(persist_directory = "/dbfs/ChromaDB", embedding_function=local_embeddings, collection_name = "game_news")

st.text_input("What's the maximum number of news you want to hear about?", key="num_doc_to_retrieve")
st.text_input("Ask a video game news related question", key="question", on_change = answer_the_question,
              args = ("qwen2.5:1.5b",  int(st.session_state.num_doc_to_retrieve)))

st.write(st.session_state['answer'])

def print_scraped_news():
    st.write(vectordb.get())

st.button("Print scraped news", on_click = print_scraped_news)

#st.write(vectordb.get())
#vectordb.delete_collection()