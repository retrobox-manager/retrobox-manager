#!/usr/bin/python3
"""Manager for the Software BATOCERA"""

import os
from libraries.constants.constants import Constants, Media, Platform, Software
from libraries.file.file_helper import FileHelper
from libraries.xml.xml_helper import XmlHelper
from manager.abstract_manager import AbstractManager

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


class BatoceraManager(AbstractManager):
    """Manager for the Software BATOCERA"""

    __PATH_ROMS = 'roms'
    __PATH_GAMELIST = 'gamelist.xml'

    __TAG_GAME = 'game'
    __TAG_PATH = 'path'
    __TAG_NAME = 'name'

    __FILE_PREFIX = './'

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

    __SOFTWARE_GAME_INFO_PRIORITY = [
        Software.BATOCERA,
        Software.SKRAPER
    ]

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

    def list_platforms(self) -> list[Platform]:
        """List platforms"""

        # Initialize result
        result: list[Platform] = []

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
                    self.__PATH_ROMS,
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

        # Get game's data
        game_data = XmlHelper.get_tag_data(
            xml_file_path=self.__retrieve_game_list_xml_path(
                platform=platform
            ),
            tag=self.__TAG_GAME,
            criteria={
                self.__TAG_NAME: game_item[Constants.UI_TABLE_KEY_COL_NAME]
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

    def retrieve_rom_file(self, platform: Platform, game_item: dict) -> str:
        """Retrieve rom file"""

        # Initialize result
        result: str = os.path.join(
            self._folder_path,
            self.__PATH_ROMS,
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

        # Add a tab to the first line if any lines exist
        if lines:
            lines[0] = '\t' + lines[0]

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

        # Copy the rom
        batocera_rom_file = os.path.join(
            self._folder_path,
            self.__PATH_ROMS,
            self.__PLATFORM_DICT_INV.get(platform, ''),
            FileHelper.retrieve_file_name(rom_file)
        )
        FileHelper.copy_file(
            source_file_path=rom_file,
            destination_file_path=batocera_rom_file
        )

        # Retrieve better game info depending on a priority
        better_game_info = None
        for software in self.__SOFTWARE_GAME_INFO_PRIORITY:
            game_info_file = game_info_files.get(software, None)
            if game_info_file is not None:
                better_game_info = FileHelper.read_file(game_info_file)
                break

        # If no game info found, finish the installation without info and media
        if better_game_info is None:
            return True

        # Install media files
        batocera_media_files = {}
        for key, media in self.__MEDIA_DICT.items():
            media_file = media_files.get(media, None)
            if media_file is None:
                continue

            # Retrieve media's folder
            media_folder = 'images'
            if media == Media.MANUAL:
                media_folder = 'manuals'
            elif media == Media.VIDEO:
                media_folder = 'videos'

            # Copy media file in software
            file_name = FileHelper.retrieve_file_basename(batocera_rom_file)
            file_name += '-'
            file_name += key
            file_name += FileHelper.retrieve_file_extension(media_file)
            batocera_media_files[media] = os.path.join(
                self._folder_path,
                self.__PATH_ROMS,
                self.__PLATFORM_DICT_INV.get(platform, ''),
                media_folder,
                file_name
            )
            FileHelper.copy_file(
                source_file_path=media_file,
                destination_file_path=batocera_media_files[media]
            )

            # Add media
            better_game_info += ""

        print(better_game_info)

        lines = [
            line for line in better_game_info.splitlines()
            if self.__FILE_PREFIX not in line and line.strip() != ""
        ]

        # Nouveau contenu à insérer
        new_tags = [
            "        \t<toto>value</toto>",
            "        \t<titi>value</titi>",
            "        \t<tata>value</tata>",
        ]

        # Insérer avant la dernière ligne
        if len(lines) >= 1:
            lines[-1:-1] = new_tags   # insertion juste avant la dernière ligne

        result = "\n".join(lines)
        print(result)

        return False
