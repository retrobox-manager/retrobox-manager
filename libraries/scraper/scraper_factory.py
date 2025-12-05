#!/usr/bin/python3
"""Scraper Factory"""


from libraries.constants.constants import Scraper
from libraries.scraper.abstract_scraper import AbstractScraper
from libraries.scraper.emu_movies.emu_movies_scraper import EmuMoviesScraper
from libraries.scraper.skraper.skraper_scraper import SkraperScraper


class ScraperFactory:
    """Scraper Factory"""

    @staticmethod
    def create(scraper: Scraper) -> AbstractScraper:
        """Create scraper"""

        match(scraper):
            case Scraper.EMU_MOVIES:
                return EmuMoviesScraper()
            case Scraper.SKRAPER:
                return SkraperScraper()
            case _:
                raise Exception('Unimplemented Scraper!')
