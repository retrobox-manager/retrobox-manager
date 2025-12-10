#!/usr/bin/python3
"""Manager for the Software LAUNCHBOX"""

import os
from libraries.constants.constants import Constants, Software
from libraries.file.file_helper import FileHelper
from libraries.xml.xml_helper import XmlHelper
from manager.abstract_manager import AbstractManager


class LaunchboxManager(AbstractManager):
    """Manager for the Software LAUNCHBOX"""

    __PATH_DATA = 'Data'
    __PATH_PLATFORMS = 'Platforms'

    __MEDIA = {
    }

    def get_enum(self) -> Software:
        """Get enum"""

        return Software.LAUNCHBOX

    def get_rom_key(self) -> str:
        """Get rom's key"""

        return ''

    def list_platforms(self) -> list:
        """List platforms"""

        platforms = []
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
            platforms.append(
                relative_path[:-len(Constants.XML_EXTENSION)]
            )

        return platforms

    def list_games(self, platform: str) -> list:
        """List games"""

        games = XmlHelper.list_tag_values(
            xml_file_path=os.path.join(
                self._folder_path,
                self.__PATH_DATA,
                self.__PATH_PLATFORMS,
                f'{platform}{Constants.XML_EXTENSION}'
            ),
            parent_tag='Game',
            tag='Title'
        )
        return games

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
