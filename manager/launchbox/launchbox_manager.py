#!/usr/bin/python3
"""Manager for the Software LAUNCHBOX"""

import os
from typing import Dict, List
from libraries.constants.constants import Constants, Media, Platform, Software
from libraries.file.file_helper import FileHelper
from libraries.xml.xml_helper import XmlHelper
from manager.abstract_manager import AbstractManager


class LaunchboxManager(AbstractManager):
    """Manager for the Software LAUNCHBOX"""

    __PATH_DATA = 'Data'
    __PATH_PLATFORMS = 'Platforms'

    __MEDIA_DICT = {
    }

    __PLATFORM_DICT = {
        'Sega Master System': Platform.SEGA_MASTERSYSTEM,
        'MegaDrive': Platform.SEGA_MEGADRIVE
    }

    __PLATFORM_DICT_INV = {v: k for k, v in __PLATFORM_DICT.items()}

    def get_enum(self) -> Software:
        """Get enum"""

        return Software.LAUNCHBOX

    def list_platforms(self) -> List[Platform]:
        """List platforms"""

        # Initialize result
        result: List[Platform] = []

        # Add platforms linked to a XML file
        for relative_path in FileHelper.list_relative_paths(
            folder_path=os.path.join(
                self._folder_path,
                self.__PATH_DATA,
                self.__PATH_PLATFORMS
            ),
            file_name='*',
            error_if_not_found=False
        ):
            if not relative_path.endswith(Constants.XML_EXTENSION):
                continue
            key = relative_path[:-len(Constants.XML_EXTENSION)]
            platform = self.__PLATFORM_DICT.get(key, None)
            if platform is not None:
                result.append(platform)

        return result

    def list_games(self, platform: Platform) -> List[str]:
        """List games"""

        # Initialize result
        result: List[str] = []

        # Retrieve game list XML path from platform
        game_list_xml_path = os.path.join(
            self._folder_path,
            self.__PATH_DATA,
            self.__PATH_PLATFORMS,
            f'{self.__PLATFORM_DICT_INV[platform]}{Constants.XML_EXTENSION}'
        )

        # Add games for the platform
        if FileHelper.is_file_exists(game_list_xml_path):
            result = XmlHelper.list_tag_values(
                xml_file_path=game_list_xml_path,
                parent_tag='Game',
                tag='Title'
            )

        return result

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
