import requests
from bs4 import BeautifulSoup


class GithubTrendExtractor:
    base_url = "https://github.com/trending/"

    def __init__(self, params, p_lang) -> None:
        self.params = params
        self.url = self.base_url + str(p_lang)

    def extract(self):
        resp = requests.get(url=self.url, params=self.params)
        return resp

    @staticmethod
    def resp2soup(resp):
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup

    def __call__(self) -> BeautifulSoup:
        resp = self.extract()
        assert resp.ok, "Error on resp"
        soup = self.resp2soup(resp)
        trending_repos = soup.find_all("article", class_="Box-row")
        return trending_repos
