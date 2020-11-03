from bs4 import BeautifulSoup
import logging
import pandas as pd
import requests

DEBUG_DEV = False

if DEBUG_DEV: logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s")

class rss_client:
    """[summary]
    """
    def __init__(self):
        pass

    def standard_parse(self,
                       ls_source: list):
        """[summary]

        Args:
            ls_source (list): list of rss feed source urls

        Returns:
            DataFrame: news feeds dataframe that has title, description, news link, image, link and published date
        """
        df = pd.DataFrame(columns = ["title", "description", "link_news", "link_image", "date"])
        for source in ls_source:
            response = requests.get(source)
            soup = BeautifulSoup(response.content, features="xml")
            # print(f"{soup.prettify()}")                                 # view output
            items = soup.findAll("item")                                  # find all entries with <item> in the parsed xml
            ls_news_items = []
            for item in items:
                news_item = {}
                news_item["title"] = item.title.text
                news_item["description"] = item.description.text
                news_item["link_news"] = item.link.text
                news_item["link_image"] = item.image.text
                news_item["date"] = item.pubDate.text
                ls_news_items.append(news_item)
            df = df.append(ls_news_items, ignore_index=True)
            if DEBUG_DEV: logging.debug(f"df total rows: {df.shape[0]}")
        return df

class db_client:
    def __init__(self, cnn):
        pass
    def write(self,conn,):
        pass