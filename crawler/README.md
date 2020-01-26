# Crawler

## Definition

A crawler is a program that visits Web sites and reads their pages and other information in order to create entries for a search engine index.

In this project, the context of the crawler module's functionality is expanded to include, API based data extraction and data manipulation solutions for on the algorithmic trading context.

## Proposed structure

- Interface layer: The part that binds to the data source and extracts raw data
- Transformation layer: This part transforms the data in a format that is supported by the contracts. (It's possible to create new contracts that are extensions of the previous one's upon discussion with the main team.)
- Storage layer: This part saves the transformed data to the database calling the respective controllers functions.

The functionalities above should be as decoupled as possible in order to promote reusability.

 An example can be found on the crawler_template.py file located inside the .crawler/twitter folder.

## Twitter Crawler Usage

python start_crawler.py TwitterCrawler (params) params are in the form key:value

Available params:
- keywords => Define the query/keyword to search for. Example: bitcoin,ethereum,doggecoin
- since => Define the date since which to search. The format is YYYY-MM-DD. Example: 2020-04-23
- until => Define the date until which to search. The format is YYYY-MM-DD. Example: 2020-04-24
- from-position => Define the position (post id) from which to search (descending).
- wait_secs => Define the wait time in seconds bettween scraping requests. The default is 5 and the code enforces values greater or equal to 1.

Examples:
python start_crawler.py TwitterCrawler keywords:bitcoin since:2020-01-01 until:2020-01-02