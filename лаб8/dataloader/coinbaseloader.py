import json
import pandas as pd
import logging
from datetime import datetime
from pandas.core.api import DataFrame
from enum import Enum
import requests

from baseloader import BaseDataLoader

class Granularity(Enum):
    ONE_MINUTE = 60
    FIVE_MINUTES = 300
    FIFTEEN_MINUTES = 900
    ONE_HOUR = 3600
    THREE_HOUR = 10800
    SIX_HOURS = 21600
    ONE_DAY = 86400

class CoinbaseLoader(BaseDataLoader):

    def __init__(self, endpoint="https://api.exchange.coinbase.com"):
        super().__init__(endpoint)

        # Створюємо об'єкт логера
        self.logger = logging.getLogger(__name__)

        # Встановлюємо рівень логування
        self.logger.setLevel(logging.INFO)

        # Створюємо форматер
        formatter = logging.Formatter('%(asctime)s - %(relativeCreated)d - %(name)s - %(funcName)s - %(levelname)s - %(levelno)s - %(pathname)s - %(message)s')

        # Створюємо хендлер, що пише у файл
        file_handler = logging.FileHandler('INFO.log')
        file_handler.setFormatter(formatter)

        # Додаємо хендлер до логера
        self.logger.addHandler(file_handler)

    def get_pairs(self) -> pd.DataFrame:
        data = self._get_req("/products")
        df = pd.DataFrame(json.loads(data))
        df.set_index('id', drop=True, inplace=True)
        self.logger.info('Pairs data retrieved successfully')  # Логуємо успішне отримання даних
        return df

    def get_stats(self, pair: str) -> pd.DataFrame:
        data = self._get_req(f"/products/{pair}")
        df = pd.DataFrame(json.loads(data), index=[0])
        self.logger.info(f'Stats for {pair} retrieved successfully')  # Логуємо успішне отримання статистики
        return df

    from datetime import datetime

# ...

    def get_historical_data(self, pair: str, begin: str, end: str, granularity: Granularity) -> DataFrame:
        begin = datetime.strptime(begin, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')

        params = {
            "start": begin.strftime('%Y-%m-%d'),
            "end": end.strftime('%Y-%m-%d'),
            "granularity": granularity.value
        }
    # ...

        # retrieve needed data from Coinbase
        data = self._get_req("/products/" + pair + "/candles", params)
        # parse response and create DataFrame from it
        df = pd.DataFrame(json.loads(data), columns=("timestamp", "low", "high", "open", "close", "volume"))
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        # use timestamp column as index
        df.set_index('timestamp', drop=True, inplace=True)
        self.logger.info(f'Historical data for {pair} from {begin} to {end} retrieved successfully')  # Логуємо успішне отримання історичних даних
        return df

if __name__ == "__main__":
    loader = CoinbaseLoader()
    data = loader.get_pairs()
    data = data.drop(['TRAC-USDT', 'APE-USD', 'AUCTION-USDT', 'CLV-USDT'])
    print(data)
    data = loader.get_stats("btc-usdt")
    print(data)
    data = loader.get_historical_data("btc-usdt", "2023-01-01", "2023-06-30", granularity=Granularity.ONE_DAY)
    print(data.head(5))

