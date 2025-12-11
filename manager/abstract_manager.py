#!/usr/bin/python3
"""Abstract Manager"""

from abc import ABC, abstractmethod
from typing import Dict, List

from libraries.constants.constants import Media, Platform, Software
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
    def list_platforms(self) -> List[Platform]:
        """List platforms"""

    @abstractmethod
    def list_games(self, platform: Platform) -> List[str]:
        """List games"""

    @abstractmethod
    def retrieve_media_files(self, platform: Platform, game: str) -> Dict[Media, str]:
        """Retrieve media files"""

    @abstractmethod
    def retrieve_rom_file(self, platform: Platform, game: str) -> str:
        """Retrieve rom file"""

    @abstractmethod
    def retrieve_game_info(self, platform: Platform, game: str) -> str:
        """Retrieve game info"""
