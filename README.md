# Search links

Project created to collects results from search engines.

## Search engine supported 

 * DuckDuckGo

## Requirements

* beautifulsoup4==4.6.0
* scrapy


    pip install -r requirements.txt

## How to use

Start DuckDuckGO search:

    scrapy crawl duckduckgo -o {OUTPUT_PATH} -a query="{SEARCH_PARAMS}"  

Example

    scrapy crawl duckduckgo -o result.json -a query="proxies free list"  


