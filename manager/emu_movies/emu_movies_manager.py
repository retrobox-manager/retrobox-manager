#!/usr/bin/python3
"""Manager for the Software EMU_MOVIES"""

from libraries.constants.constants import Media, Platform, Software
from manager.abstract_manager import AbstractManager

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


class EmuMoviesManager(AbstractManager):
    """Manager for the Software EMU_MOVIES"""

    __MEDIA_DICT = {
        'Background': Media.FAN_ART,
        'Box': Media.BOX_2D_FRONT,
        'Box_3D': Media.BOX_3D,
        'Box_Full': Media.BOX_2D_FRONT,
        'BoxBack': Media.BOX_2D_BACK,
        'Cart': Media.BOX_2D_FRONT,
        'Cart_3D': Media.BOX_3D,
        'CartTop': Media.BOX_2D_FRONT,
        'Logos': Media.LOGO,
        'Marquee': Media.LOGO,
        'Snap': Media.SCREENSHOT_GAME,
        'Title': Media.SCREENSHOT_TITLE,
        'Video_MP4_HI_QUAL': Media.VIDEO
    }

    __PLATFORM_DICT = {
        'mastersystem': Platform.SEGA_MASTERSYSTEM,
        'megadrive': Platform.SEGA_MEGADRIVE
    }

    def get_enum(self) -> Software:
        """Get enum"""

        return Software.EMU_MOVIES

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
