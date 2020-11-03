from datetime import date
from utilities import nse_client
import logging

DEBUG_DEV = False
if DEBUG_DEV: logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s")

nse = nse_client()


# Get the latest tradeable NSE stock list
# tickers = nse.get_tickers()
if DEBUG_DEV: logging.debug(f"total tickers: {len(tickers)}")

# Download historics data
df = nse.get_historical(ticker="BANKNIFTY",
                        date_end=date.today(),
                        date_start=date(2020,10,1),
                        index=True)
print(df.dtypes)
print(df.info)
# print(df.tail())