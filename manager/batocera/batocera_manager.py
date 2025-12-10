#!/usr/bin/python3
"""Manager for the Software BATOCERA"""

import os
from libraries.constants.constants import Media, Software
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

    __MEDIA = {
        'image': Media.SCREENSHOT_GAME,
        'marquee': Media.LOGO,
        'thumbnail': Media.BOX_3D,
        'fanart': Media.FAN_ART,
        'titleshot': Media.SCREENSHOT_TITLE,
        'boxback': Media.BOX_2D_BACK,
        'manual': Media.MANUAL,
        'video': Media.VIDEO
    }

    def __retrieve_game_list_xml_path(
        self,
        platform: str
    ) -> str:
        """Retrieve the path for XML file listing games"""

        return os.path.join(
            self._folder_path,
            self.__PATH_ROMS,
            platform,
            self.__PATH_GAMELIST
        )

    def get_enum(self) -> Software:
        """Get enum"""

        return Software.BATOCERA

    def get_rom_key(self) -> str:
        """Get rom's key"""

        return 'path'

    def list_platforms(self) -> list:
        """List platforms"""

        platforms = []
        for platform in FileHelper.list_sub_directories(
            folder_path=os.path.join(
                self._folder_path,
                self.__PATH_ROMS
            )
        ):
            if not FileHelper.is_file_exists(
                self.__retrieve_game_list_xml_path(
                    platform=platform
                )
            ):
                continue

            platforms.append(platform)

        return platforms

    def list_games(self, platform: str) -> list:
        """List games"""

        games = XmlHelper.list_tag_values(
            xml_file_path=os.path.join(
                self.__retrieve_game_list_xml_path(
                    platform=platform
                )
            ),
            parent_tag=self.__TAG_GAME,
            tag=self.__TAG_NAME
        )

        return games

    def retrieve_game_files(self, platform: str, game: str) -> dict:
        """Retrieve game files"""

        # Initialize result
        result = {}

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

        for key, value in game_data.items():
            if value.startswith(self.__FILE_PREFIX):
                result[key] = os.path.join(
                    self._folder_path,
                    self.__PATH_ROMS,
                    platform,
                    value[2:].replace('/', '\\')
                )

        return result

    def retrieve_game_info(self, platform: str, game: str) -> str:
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
