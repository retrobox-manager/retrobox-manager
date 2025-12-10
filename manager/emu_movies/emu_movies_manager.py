#!/usr/bin/python3
"""Manager for the Software EMU_MOVIES"""

from libraries.constants.constants import Media, Software
from manager.abstract_manager import AbstractManager


class EmuMoviesManager(AbstractManager):
    """Manager for the Software EMU_MOVIES"""

    __MEDIA = {
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
