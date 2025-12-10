#!/usr/bin/python3
"""Manager for the Software SKRAPER"""

from libraries.constants.constants import Media, Software
from manager.abstract_manager import AbstractManager


class SkraperManager(AbstractManager):
    """Manager for the Software SKRAPER"""

    __MEDIA = {
        'box2dfront': Media.BOX_2D_FRONT,
        'box2dside': Media.BOX_2D_SIDE,
        'box2dback': Media.BOX_2D_BACK,
        'box3d': Media.BOX_3D,
        'boxtexture': Media.BOX_2D_BACK,
        'support': Media.SUPPORT,
        'supporttexture': Media.SUPPORT,
        'wheel': Media.LOGO,
        'wheelcarbon': Media.LOGO_CARBON,
        'wheelsteel': Media.LOGO_STEEL,
        'steamgrid': Media.LOGO,
        'screenmarquee': Media.LOGO,
        'screenmarqueesmall': Media.LOGO,
        'marquee': Media.LOGO,
        'screenshot': Media.SCREENSHOT_GAME,
        'screenshottitle': Media.SCREENSHOT_TITLE,
        'fanart': Media.FAN_ART,
        'mix': Media.SCREENSHOT_GAME,
        'images': Media.SCREENSHOT_GAME,
        'manuals': Media.MANUAL,
        'videos': Media.VIDEO
    }

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
