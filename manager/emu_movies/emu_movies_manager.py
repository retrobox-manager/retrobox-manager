#!/usr/bin/python3
"""Manager for the Software EMU_MOVIES"""

from typing import Dict, List
from libraries.constants.constants import Media, Platform, Software
from manager.abstract_manager import AbstractManager


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

    def list_platforms(self) -> List[Platform]:
        """List platforms"""

        return []

    def list_games(self, platform: Platform) -> List[str]:
        """List games"""

        print(platform)

        return []

    def retrieve_media_files(self, platform: Platform, game: str) -> Dict[Media, str]:
        """Retrieve media files"""

        print(platform)
        print(game)

        return {}

    def retrieve_rom_file(self, platform: Platform, game: str) -> str:
        """Retrieve rom file"""

        print(platform)
        print(game)

        return None

    def retrieve_game_info(self, platform: Platform, game: str) -> str:
        """Retrieve game info"""

        print(platform)
        print(game)

        return ''
