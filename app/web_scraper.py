import asyncio
from crawl4ai import *
import ollama
import re
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import hashlib
#had to run playwright install for first time use

sitemap = "https://www.ign.com/rss/news/sitemap"
url = "https://www.ign.com/articles/dragon-age-the-veilguard-patch-notes-sure-make-it-sound-like-biowares-basically-done-with-the-game-now"


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
    response = ollama.chat(model = model, messages = [
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
    local_embeddings = OllamaEmbeddings(model = "all-minilm")
    ids = [hashlib.sha256(url.encode()).hexdigest() for url in news]
    vectorestore = Chroma.from_texts(texts = results, embedding= local_embeddings, collection_name = "game_news", ids = ids)

if __name__ == "__main__":
    news = get_ign_urls(sitemap)
    news = news[:3]
    results = main(news, model = "smollm:135m")
    store_results(news, results)