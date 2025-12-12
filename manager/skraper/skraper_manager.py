#!/usr/bin/python3
"""Manager for the Software SKRAPER"""

import os
from libraries.constants.constants import Constants, Media, Platform, Software
from libraries.file.file_helper import FileHelper
from libraries.xml.xml_helper import XmlHelper
from manager.abstract_manager import AbstractManager

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


class SkraperManager(AbstractManager):
    """Manager for the Software SKRAPER"""

    __PATH_GAMELIST = 'gamelist.xml'

    __TAG_GAME = 'game'
    __TAG_NAME = 'name'
    __TAG_PATH = 'path'

    __FILE_PREFIX = './'

    __MEDIA_PATH = 'media'

    __MEDIA_DICT = {
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
            self.__PLATFORM_DICT_INV.get(platform, ''),
            self.__PATH_GAMELIST
        )

    def get_enum(self) -> Software:
        """Get enum"""

        return Software.SKRAPER

    def list_platforms(self) -> list[Platform]:
        """List platforms"""

        # Initialize result
        result: list[Platform] = []

        # Add platforms linked to a sub directory
        for folder in FileHelper.list_sub_directories(
            folder_path=self._folder_path
        ):
            platform = self.__PLATFORM_DICT.get(folder, None)
            if platform is not None:
                result.append(platform)

        return result

    def list_games_with_rom(self, platform: Platform) -> dict[str, str]:
        """List games in a dictionary where the key is the rom and the value is the name"""

        # Initialize result
        result: dict[str, str] = {}

        # Retrieve game list XML path from platform
        game_list_xml_path = os.path.join(
            self.__retrieve_game_list_xml_path(
                platform=platform
            )
        )

        # Add games for the platform
        if FileHelper.is_file_exists(game_list_xml_path):
            # Retrieve tags values
            tag_path_values = XmlHelper.list_tag_values(
                xml_file_path=game_list_xml_path,
                parent_tag=self.__TAG_GAME,
                tag=self.__TAG_PATH
            )
            tag_name_values = XmlHelper.list_tag_values(
                xml_file_path=game_list_xml_path,
                parent_tag=self.__TAG_GAME,
                tag=self.__TAG_NAME
            )

            # Error if BDD inconsistent
            if len(tag_name_values) != len(tag_name_values):
                raise Exception(f'{game_list_xml_path} is inconsistent!')

            for rom_path in tag_path_values:
                # Check if the rom file exists
                rom_file = os.path.join(
                    self._folder_path,
                    self.__PLATFORM_DICT_INV.get(platform, ''),
                    rom_path
                )
                if FileHelper.is_file_exists(rom_file):
                    result[FileHelper.retrieve_file_name(rom_file)] = tag_name_values[
                        tag_path_values.index(rom_path)
                    ]

        return result

    def retrieve_media_files(self, platform: Platform, game_item: dict) -> dict[Media, str]:
        """Retrieve media files"""

        # Initialize result
        result: dict[Media, str] = {}

        # Retrieve media's path
        media_path = os.path.join(
            self._folder_path,
            self.__PLATFORM_DICT_INV.get(platform, ''),
            self.__MEDIA_PATH
        )

        # Add media for the game
        for folder in FileHelper.list_sub_directories(
            folder_path=media_path
        ):
            media = self.__MEDIA_DICT.get(folder, None)
            if media is None:
                continue

            relative_paths = FileHelper.list_relative_paths(
                folder_path=os.path.join(
                    media_path,
                    folder
                ),
                file_name='*',
                error_if_not_found=False
            )

            if len(relative_paths) == 0:
                continue

            result[media] = os.path.join(
                media_path,
                folder,
                relative_paths[0]
            )

        return result

    def retrieve_rom_file(self, platform: Platform, game_item: dict) -> str:
        """Retrieve rom file"""

        # Initialize result
        result: str = os.path.join(
            self._folder_path,
            self.__PLATFORM_DICT_INV.get(platform, ''),
            game_item[Constants.UI_TABLE_KEY_COL_ROM]
        )

        # Check that rom file exists
        if not FileHelper.is_file_exists(result):
            return None

        return result

    def retrieve_game_info(self, platform: Platform, game_item: dict) -> str:
        """Retrieve game info"""

        # Initialize result
        result = ''

        game_data = XmlHelper.get_tag_content(
            xml_file_path=self.__retrieve_game_list_xml_path(
                platform=platform
            ),
            tag=self.__TAG_GAME,
            criteria={
                self.__TAG_NAME: game_item[Constants.UI_TABLE_KEY_COL_NAME]
            }
        )

        # Filter out lines containing the file prefix
        lines = [
            line for line in game_data.splitlines()
            if self.__FILE_PREFIX not in line and line.strip() != ""
        ]

        # Add 2 spaces to the first line if any lines exist
        if lines:
            lines[0] = '  ' + lines[0]

        result = '\n'.join(lines)

        return result

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
