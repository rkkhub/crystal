from datetime import date
from functools import wraps
from mysql import connector
from nsepy import get_history
from nsetools import Nse
import logging
import os
import pandas as pd


# ------------------------------------------------------decorators
def with_connection(host: str,
                    username: str,
                    password: str,
                    schema: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            conn = connector.connect(host=host,
                                     user=username,
                                     passwd=password,
                                     database=schema)
            try:
                return func(*args, **kwargs, conn=conn)
            finally:
                conn.close()
        return wrapper
    return decorator


# ------------------------------------------------------NSE utility
class nse_client:
    def __init__(self):
        pass

    def get_tickers(self):
        nse = Nse()
        all_ticker = nse.get_stock_codes(cached=False)
        all_ticker.pop("SYMBOL", None)
        return tuple(all_ticker)
    
    def get_historical(self,
                       ticker: str,
                       date_end: date = date.today(),
                       date_start: date = date(1993,4,1),
                       index=False):
        """[summary]

        Args:
            ticker (str): [description]
            date_end (date, optional): [description]. Defaults to date.today().
            date_start (date, optional): [description]. Defaults to date(1993,4,1).

        Returns:
            dataframe: [description]
        """
        data = get_history(symbol=f"{ticker}",
                           start=date_start,
                           end=date_end,
                           index=index)
        return data

# ------------------------------------------------------database utility
class db_client():
            # cols = symbol, series, close_prev, ope, high, low, last, close, vwap, volume, turnover, trades, volume_deliverable, deleverable_pcnt
    def __init__(self):
        pass


    @with_connection(host=os.environ["DB_HOST"],
                     username=os.environ["DB_USER"],
                     password=os.environ["DB_PASS"],
                     schema=os.environ["DB_SCHEMA"])
    def write_equity(self,
                         df,
                         conn,
                         table: str= "equity_historical"):
        total_insert = 0
        cursor = conn.cursor()
        for index, row in df.iterrows():
            query = f"""INSERT INTO {table} (date, symbol, series, close_prev,
                                                open, high, low,
                                                last, close, vwap,
                                                volume, turnover, trades,
                                                volume_deliverable, volume_deleverable_perct) 
                    VALUES ("{index}", "{row['Symbol']}", "{row['Series']}", {row['Prev Close']},
                            {row['Open']}, {row['High']}, {row['Low']},
                            {row['Last']}, {row['Close']}, {row['VWAP']},
                            {row['Volume']}, {row['Turnover']}, {row['Trades']},
                            {row['Deliverable Volume']}, {row['%Deliverable']});"""
            cursor.execute(query)
            total_insert += cursor.rowcount()
        return total_insert
    
    @with_connection(host=os.environ["DB_HOST"],
                     username=os.environ["DB_USER"],
                     password=os.environ["DB_PASS"],
                     schema=os.environ["DB_SCHEMA"])
    def read_equity(self,
                        columns: str,
                        conn,
                        table: str = "equity_historical"):
        query = f"SELECT {columns} from {table} order by date desc;"
        cursor = conn.cursor()
        result = cursor.fetchall(query)
        df = pd.dataframe(result, columns = tuple(columns))
        return df 
        
class utility:
    def __init__(self):
        pass
    
    def get_startdate(self, symbol, symbol_type: str ="equity"):
        db = db_client()
        if symbol_type.lower() == "equity":
            df = db.read_equity(columns="date, symbol")
            if df.shape[0] > 0:
                start_date = df["date"].tolist()[0] #convert to date format
            else:
                start_date = date(1993,4,1)
            return start_date
        else:
            df = db.read_index(columns="date, symbol")
            if df.shape[0] > 0:
                start_date = df["date"].tolist()[0] #convert to date format
            else:
                start_date = date(1993,4,1)
            return start_date



