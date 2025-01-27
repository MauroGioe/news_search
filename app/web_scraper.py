import asyncio
from crawl4ai import *
import ollama
import re
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import hashlib
from ollama import Client
ollama_client = Client(host='http://ollama:11434/')
#had to run playwright install for first time use

sitemap = "https://www.ign.com/rss/news/sitemap"

async def scrape_markdown(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url= url
        )
        return result.markdown



def get_ign_urls(sitemap):
    try:
        sitemap_urls = asyncio.run(scrape_markdown(sitemap))
        sitemap_urls = re.findall("<loc>(.*?)</loc>", sitemap_urls)
        return sitemap_urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []




def summarize_news(markdown, model, context_window = 20000):
    response = ollama_client.chat(model = model, messages = [
      {
        'role': 'user',
        'content': f"summarize the main news from the following markdown and add the news time release to the end. Markdown: {markdown}",
      },
    ],  options={"temperature":0, "num_ctx":context_window})
    return response["message"]["content"]


def main (news, model):
    results = []
    for url in news:
        markdown = asyncio.run(scrape_markdown(url))
        summary = summarize_news(markdown, model)
        results.append(summary)
    return results


def store_results(news, results):
    local_embeddings = OllamaEmbeddings(model = "all-minilm", base_url = "http://ollama:11434/")
    ids = [hashlib.sha256(url.encode()).hexdigest() for url in news]
    vectorestore = Chroma.from_texts(persist_directory = "/dbfs/ChromaDB", texts = results, embedding= local_embeddings,
                                     collection_name = "game_news", ids = ids)
    print("DB saved")
if __name__ == "__main__":
    news = get_ign_urls(sitemap)
    news = news[:5]
    results = main(news, model = "smollm:135m")
    store_results(news, results)