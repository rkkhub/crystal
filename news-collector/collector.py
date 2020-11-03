from pathlib import Path
from utilities import rss_client
import logging
import pandas as pd

DEBUG_DEV = True
file_rss = Path("rss.csv")

if DEBUG_DEV: logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s")
rss = rss_client()
df_rss = pd.read_csv(file_rss)
ls_rss = df_rss["link"].tolist()
if DEBUG_DEV: logging.debug(f"total rss sources: {len(ls_rss)}")

df = rss.standard_parse(ls_source = ls_rss)


if DEBUG_DEV: logging.debug(f"news feed sample: \n{df.head(5)}")

# dataframe to database

