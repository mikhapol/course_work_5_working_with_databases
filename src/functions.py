import requests


class HeadHunterAPI:
    """
    Класс для взаимодействия с API HeadHunter
    """

    def __init__(self, keyword, page=0):
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "text": keyword,
            "page": page
        }

    def get_request(self):
        return requests.get(self.url, params=self.params)
