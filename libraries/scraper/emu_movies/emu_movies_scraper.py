#!/usr/bin/python3
"""Scraper for EMU_MOVIES"""

from libraries.constants.constants import Scraper
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.scraper.abstract_scraper import AbstractScraper


class EmuMoviesScraper(AbstractScraper):
    """Scraper for EMU_MOVIES"""

    def __init__(self):
        """Initialize Scraper"""

        self.__folder_path = Context.get_scraper_path(
            scraper=self.get_id()
        )

    def get_id(self) -> Scraper:
        """Get id"""

        return Scraper.EMU_MOVIES

    def list_platforms(self) -> list:
        """List platforms"""

        platforms = []
        for platform in FileHelper.list_sub_directories(
            folder_path=self.__folder_path
        ):
            platforms.append(platform)

        return platforms
