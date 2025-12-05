#!/usr/bin/python3
"""Abstract Scraper"""

from abc import ABC, abstractmethod

from libraries.constants.constants import Scraper


class AbstractScraper(ABC):
    """Abstract Scraper (Common for all scrapers)"""

    @abstractmethod
    def get_id(self) -> Scraper:
        """Get id"""

    @abstractmethod
    def list_platforms(self) -> list:
        """List platforms"""
