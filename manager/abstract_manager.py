#!/usr/bin/python3
"""Abstract Manager"""

from abc import ABC, abstractmethod

from libraries.constants.constants import Software
from libraries.context.context import Context


class AbstractManager(ABC):
    """Abstract manager (Common for all softwares)"""

    def __init__(self):
        """Initialize Manager"""

        self._folder_path = Context.get_software_path(
            software=self.get_enum()
        )

    def get_id(self) -> str:
        """Get id"""

        return self.get_enum().value.lower()

    @abstractmethod
    def get_enum(self) -> Software:
        """Get enum"""

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
