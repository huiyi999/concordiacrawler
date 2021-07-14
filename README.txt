1. pip install Scrapy
   installs Scrapy
2. pip install beautifulsoup4
   installs beautifulsoup4

3. run concordiacrawler/debug_crawler.py
   sets the value of items scraped to test and debug
4. run driver.py
   starts to execute preprocess.py and spimi.py,
   before run it, please check "output" directory exists, if yes delete it, (os.remove("output/"))
5. run query_run.py
   starts to execute query.py
6. 'output/' directory: saves the blocks and the final index is in "output/MERGED_BLOCKS/Merged_Blocks.txt"
7. Returns.txt: saves the results for query