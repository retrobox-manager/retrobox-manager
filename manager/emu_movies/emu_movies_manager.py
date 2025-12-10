#!/usr/bin/python3
"""Manager for the Software EMU_MOVIES"""

from libraries.constants.constants import Software
from manager.abstract_manager import AbstractManager


class EmuMoviesManager(AbstractManager):
    """Manager for the Software EMU_MOVIES"""

    def get_enum(self) -> Software:
        """Get enum"""

        return Software.EMU_MOVIES

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
