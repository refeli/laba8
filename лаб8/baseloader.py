from datetime import datetime
import requests
import pandas as pd
import logging

class BaseDataLoader:

    def __init__(self, endpoint=None):
        self._base_url = endpoint

        # Створюємо об'єкт логера
        self.logger = logging.getLogger(__name__)

        # Встановлюємо рівень логування
        self.logger.setLevel(logging.DEBUG)

        # Створюємо форматер
        formatter = logging.Formatter('%(asctime)s - %(relativeCreated)d - %(name)s - %(funcName)s - %(levelname)s - %(levelno)s - %(pathname)s - %(message)s')

        # Створюємо хендлер, що пише у файл
        file_handler = logging.FileHandler('logfi.log')
        file_handler.setFormatter(formatter)

        # Додаємо хендлер до логера
        self.logger.addHandler(file_handler)

    def _get_req(self, resource, params=None):
        req_url = self._base_url + resource
        if params is not None:
            response = requests.get(req_url, params=params)
        else:
            response = requests.get(req_url)
        if response.status_code != 200:
            msg = f"Unable to request data from {req_url}, status: {req_url.status}"
            if response.text and response.text.message:
                msg += f", message: {response.text.message}"
            self.logger.error(msg)  # Логуємо помилку
            raise RuntimeError(msg)
        self.logger.info(f"Successful request to {req_url}")  # Логуємо успішний запит
        return response.text

if __name__ == "__main__":
    loader = BaseDataLoader()
