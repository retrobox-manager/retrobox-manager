#!/usr/bin/python3
"""Abstract FrontEnd"""

from abc import ABC, abstractmethod

from libraries.constants.constants import FrontEnd


class AbstractFrontEnd(ABC):
    """Abstract FrontEnd (Common for all frontends)"""

    @abstractmethod
    def get_enum(self) -> FrontEnd:
        """Get enum"""

    @abstractmethod
    def get_id(self) -> str:
        """Get id"""

    @abstractmethod
    def get_rom_key(self) -> str:
        """Get rom's key"""

    @abstractmethod
    def list_platforms(self) -> list:
        """List platforms"""

    @abstractmethod
    def list_games(self, platform: str) -> list:
        """List games"""

    @abstractmethod
    def retrieve_game_files(self, platform: str, game: str) -> dict:
        """Retrieve game files"""

    @abstractmethod
    def retrieve_game_info(self, platform: str, game: str) -> str:
        """Retrieve game info"""
