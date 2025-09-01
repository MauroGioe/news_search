# news_search
This project represents a modern approach to web scraping thanks to the combination of the library crawl4ai
for the extraction of website markdowns and the use of large language models for the extraction
of information from such markdowns.

## Usage

1) Start the containers

Run the following command in the project directory

```
docker-compose up
```
Once the docker command is complete, you have to wait for the LLMs to be downloaded, it should take around 10 minutes. You can check the
progresses by consulting the ollama container logs.
2) Try it out

Navigate to http://localhost:8501/ in your web browser and insert in the text box a
video game related question (e.g. "can you tell me the latest news about <video game/console name>?").
The news come from https://www.ign.com/rss/news/sitemap, the latest five news are extracted
each time you click on the button "Scrape video game news", it has to be clicked at least once.
The model being used for answering the user questions is relatively small, so it may hallucinate, using bigger models leads
to RAM usage problems.