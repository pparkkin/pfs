import os
import os.path

from scrape_games import Scraper as GameScraper
from scrape_teams import Scraper as TeamScraper

class Scraper:
    def __init__(self, url, out_path):
        self._url = url
        self._out_path = out_path
    def scrape_season(self, y):
        self.validate_path()

        g_scraper = GameScraper(self._url, self._out_path)
        g_scraper.scrape_games(y)

        t_scraper = TeamScraper(self._url, self._out_path)
        t_scraper.scrape_teams(y)
    def validate_path(self):
        if not os.path.isdir(self._out_path):
            os.mkdir(self._out_path)
            return True
        return True

