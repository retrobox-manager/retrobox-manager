#!/usr/bin/python3
"""Manager for the Software LAUNCHBOX"""

from libraries.constants.constants import Media, Platform, Software
from manager.abstract_manager import AbstractManager

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


class LaunchboxManager(AbstractManager):
    """Manager for the Software LAUNCHBOX"""

    __MEDIA_DICT = {
    }

    __PLATFORM_DICT = {
        'Sega Master System': Platform.SEGA_MASTERSYSTEM,
        'MegaDrive': Platform.SEGA_MEGADRIVE
    }

    def get_enum(self) -> Software:
        """Get enum"""

        return Software.LAUNCHBOX

    def list_platforms(self) -> list[Platform]:
        """List platforms"""

        return []

    def list_games_with_rom(self, platform: Platform) -> dict[str, str]:
        """List games in a dictionary where the key is the rom and the value is the name"""

        print(platform)

        return {}

    def retrieve_media_files(self, platform: Platform, game_item: dict) -> dict[Media, str]:
        """Retrieve media files"""

        print(platform)
        print(game_item)
        print(self.__MEDIA_DICT)
        print(self.__PLATFORM_DICT)

        return {}

    def retrieve_rom_file(self, platform: Platform, game_item: dict) -> str:
        """Retrieve rom file"""

        print(platform)
        print(game_item)

        return ''

    def retrieve_game_info(self, platform: Platform, game_item: dict) -> str:
        """Retrieve game info"""

        print(platform)
        print(game_item)

        return ''

    def uninstall_game(self, platform: Platform, game_item: dict) -> bool:
        """Uninstall game"""

        print(platform)
        print(game_item)

        return False

    def install_game(
        self,
        platform: Platform,
        game_item: dict,
        media_files: dict[Media, str],
        game_info_files: dict[Software, str],
        rom_file: str
    ) -> bool:
        """Install game with the specified media files, game info files and rom file"""

        print(platform)
        print(game_item)
        print(media_files)
        print(game_info_files)
        print(rom_file)

        return False
