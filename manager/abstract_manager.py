#!/usr/bin/python3
"""Abstract Manager"""

from abc import ABC, abstractmethod

from libraries.constants.constants import Media, Platform, Software
from libraries.context.context import Context

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


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
    def list_platforms(self) -> list[Platform]:
        """List platforms"""

    @abstractmethod
    def list_games_with_rom(self, platform: Platform) -> dict[str, str]:
        """List games in a dictionary where the key is the rom and the value is the name"""

    @abstractmethod
    def retrieve_media_files(self, platform: Platform, game_item: dict) -> dict[Media, str]:
        """Retrieve media files"""

    @abstractmethod
    def retrieve_rom_file(self, platform: Platform, game_item: dict) -> str:
        """Retrieve rom file"""

    @abstractmethod
    def retrieve_game_info(self, platform: Platform, game_item: dict) -> str:
        """Retrieve game info"""

    @abstractmethod
    def uninstall_game(self, platform: Platform, game_item: dict) -> bool:
        """Uninstall game"""

    @abstractmethod
    def install_game(
        self,
        platform: Platform,
        game_item: dict,
        media_files: dict[Media, str],
        game_info_files: dict[Software, str],
        rom_file: str
    ) -> bool:
        """Install game with the specified media files, game info files and rom file"""
