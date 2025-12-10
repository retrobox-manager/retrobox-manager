#!/usr/bin/python3
"""Manager for the Software SKRAPER"""

from libraries.constants.constants import Software
from manager.abstract_manager import AbstractManager


class SkraperManager(AbstractManager):
    """Manager for the Software SKRAPER"""

    def get_enum(self) -> Software:
        """Get enum"""

        return Software.SKRAPER

    def get_rom_key(self) -> str:
        """Get rom's key"""

        return ''

    def list_platforms(self) -> list:
        """List platforms"""

        return []

    def list_games(self, platform: str) -> list:
        """List games"""

        print(platform)

        return []

    def retrieve_game_files(self, platform: str, game: str) -> dict:
        """Retrieve game files"""

        print(platform)
        print(game)

        return {}

    def retrieve_game_info(self, platform: str, game: str) -> str:
        """Retrieve game info"""

        print(platform)
        print(game)

        return ''
