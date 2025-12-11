#!/usr/bin/python3
"""Manager for the Software BATOCERA"""

import os
from typing import Dict, List
from libraries.constants.constants import Media, Platform, Software
from libraries.file.file_helper import FileHelper
from libraries.xml.xml_helper import XmlHelper
from manager.abstract_manager import AbstractManager


class BatoceraManager(AbstractManager):
    """Manager for the Software BATOCERA"""

    __PATH_ROMS = 'roms'
    __PATH_GAMELIST = 'gamelist.xml'

    __TAG_GAME = 'game'
    __TAG_NAME = 'name'

    __FILE_PREFIX = './'

    __ROM_KEY = 'path'

    __MEDIA_DICT = {
        'image': Media.SCREENSHOT_GAME,
        'marquee': Media.LOGO,
        'thumbnail': Media.BOX_3D,
        'fanart': Media.FAN_ART,
        'titleshot': Media.SCREENSHOT_TITLE,
        'boxback': Media.BOX_2D_BACK,
        'bezel': Media.BEZEL,
        'manual': Media.MANUAL,
        'video': Media.VIDEO
    }

    __PLATFORM_DICT = {
        'mastersystem': Platform.SEGA_MASTERSYSTEM,
        'megadrive': Platform.SEGA_MEGADRIVE
    }

    __PLATFORM_DICT_INV = {v: k for k, v in __PLATFORM_DICT.items()}

    def __retrieve_game_list_xml_path(
        self,
        platform: Platform
    ) -> str:
        """Retrieve the path for XML file listing games"""

        return os.path.join(
            self._folder_path,
            self.__PATH_ROMS,
            self.__PLATFORM_DICT_INV.get(platform, ''),
            self.__PATH_GAMELIST
        )

    def get_enum(self) -> Software:
        """Get enum"""

        return Software.BATOCERA

    def list_platforms(self) -> List[Platform]:
        """List platforms"""

        # Initialize result
        result: List[Platform] = []

        # Add platforms linked to a sub directory
        for folder in FileHelper.list_sub_directories(
            folder_path=os.path.join(
                self._folder_path,
                self.__PATH_ROMS
            )
        ):
            platform = self.__PLATFORM_DICT.get(folder, None)
            if platform is not None:
                result.append(platform)

        return result

    def list_games(self, platform: Platform) -> List[str]:
        """List games"""

        # Initialize result
        result: List[str] = []

        # Retrieve game list XML path from platform
        game_list_xml_path = os.path.join(
            self.__retrieve_game_list_xml_path(
                platform=platform
            )
        )

        # Add games for the platform
        if FileHelper.is_file_exists(game_list_xml_path):
            result = XmlHelper.list_tag_values(
                xml_file_path=game_list_xml_path,
                parent_tag=self.__TAG_GAME,
                tag=self.__TAG_NAME
            )

        return result

    def retrieve_media_files(self, platform: Platform, game: str) -> Dict[Media, str]:
        """Retrieve media files"""

        # Initialize result
        result: Dict[Media, str] = {}

        # Get game's data
        game_data = XmlHelper.get_tag_data(
            xml_file_path=self.__retrieve_game_list_xml_path(
                platform=platform
            ),
            tag=self.__TAG_GAME,
            criteria={
                self.__TAG_NAME: game
            }
        )

        # Add media for the game
        for key, value in game_data.items():
            media = self.__MEDIA_DICT.get(key, None)
            if media is None:
                continue
            result[media] = os.path.join(
                self._folder_path,
                self.__PATH_ROMS,
                self.__PLATFORM_DICT_INV.get(platform, ''),
                value[2:].replace('/', '\\')
            )

        return result

    def retrieve_rom_file(self, platform: Platform, game: str) -> str:
        """Retrieve rom file"""

        # Initialize result
        result: str = None

        # Get game's data
        game_data = XmlHelper.get_tag_data(
            xml_file_path=self.__retrieve_game_list_xml_path(
                platform=platform
            ),
            tag=self.__TAG_GAME,
            criteria={
                self.__TAG_NAME: game
            }
        )

        if self.__ROM_KEY in game_data:
            result = os.path.join(
                self._folder_path,
                self.__PATH_ROMS,
                self.__PLATFORM_DICT_INV.get(platform, ''),
                game_data[self.__ROM_KEY][2:].replace('/', '\\')
            )

        return result

    def retrieve_game_info(self, platform: Platform, game: str) -> str:
        """Retrieve game info"""

        # Initialize result
        result = ''

        game_data = XmlHelper.get_tag_content(
            xml_file_path=self.__retrieve_game_list_xml_path(
                platform=platform
            ),
            tag=self.__TAG_GAME,
            criteria={
                self.__TAG_NAME: game
            }
        )

        result = '\n'.join(
            line for line in game_data.splitlines() if self.__FILE_PREFIX not in line
        )

        return result
