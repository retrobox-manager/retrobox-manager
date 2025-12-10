#!/usr/bin/python3
"""Scraper for SKRAPER"""

from libraries.constants.constants import Scraper
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from scraper.abstract_scraper import AbstractScraper


class SkraperScraper(AbstractScraper):
    """Scraper for SKRAPER"""

    def __init__(self):
        """Initialize Scraper"""

        self.__folder_path = Context.get_scraper_path(
            scraper=self.get_enum()
        )

    def get_enum(self) -> Scraper:
        """Get enum"""

        return Scraper.SKRAPER

    def get_id(self) -> str:
        """Get id"""

        return self.get_enum().value.lower()

    def list_platforms(self) -> list:
        """List platforms"""

        platforms = []
        for platform in FileHelper.list_sub_directories(
            folder_path=self.__folder_path
        ):
            platforms.append(platform)

        return platforms
