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

    __TAG_GAMES = 'gameList'
    __TAG_GAME = 'game'
    __TAG_NAME = 'name'
    __TAG_PATH = 'path'

    __MEDIA_PATH = 'media'

    __FILE_PREFIX = './'
    __PATH_SEPARATOR = '/'

    __PARENT_PREFIX = '  '
    __CHILD_PREFIX = '    '

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
        'xbox360': Platform.MICROSOFT_XBOX360,
        'n64': Platform.NINTENDO_64,
        'gamecube': Platform.NINTENDO_GAME_CUBE,
        'dreamcast': Platform.SEGA_DREAMCAST,
        'mastersystem': Platform.SEGA_MASTERSYSTEM,
        'megadrive': Platform.SEGA_MEGADRIVE,
        'ps2': Platform.SONY_PLAYSTATION_2
    }

    __PLATFORM_DICT_INV = {v: k for k, v in __PLATFORM_DICT.items()}

    __SOFTWARE_GAME_INFO_PRIORITY = [
        Software.SKRAPER,
        Software.BATOCERA
    ]

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

    def __build_game_criteria(self, game_item: dict) -> dict[str, str]:
        """Build criteria to find a game"""

        return {
            self.__TAG_PATH: self.__FILE_PREFIX +
            game_item[Constants.UI_TABLE_KEY_COL_ROM]
        }

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
        else:
            # List roms
            for rom_file in FileHelper.list_sub_directories(
                folder_path=os.path.join(
                    self._folder_path,
                    self.__PLATFORM_DICT_INV.get(platform, ''),
                )
            ):
                result[rom_file] = ''

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
            parent_tag=self.__TAG_GAMES,
            tag=self.__TAG_GAME,
            criteria=self.__build_game_criteria(game_item)
        )

        if game_data is None:
            return result

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

        # Delete media files
        media_files = self.retrieve_media_files(
            platform=platform,
            game_item=game_item
        )
        for media_file in media_files.values():
            FileHelper.delete_file(
                file_path=media_file
            )

        # Delete rom file
        FileHelper.delete_file(
            file_path=self.retrieve_rom_file(
                platform=platform,
                game_item=game_item
            )
        )

        # Delete tag for the game
        return XmlHelper.delete_tag(
            xml_file_path=self.__retrieve_game_list_xml_path(
                platform=platform
            ),
            parent_tag=self.__TAG_GAMES,
            tag=self.__TAG_GAME,
            criteria=self.__build_game_criteria(game_item)
        )

    def install_game(
        self,
        platform: Platform,
        game_item: dict,
        media_files: dict[Media, str],
        game_info_files: dict[Software, str],
        rom_file: str
    ) -> bool:
        """Install game with the specified media files, game info files and rom file"""

        # Uninstall before installing
        self.uninstall_game(
            platform=platform,
            game_item=game_item
        )

        # Initialize fields to add
        fields_to_add = {}

        # Copy the rom
        skraper_rom_file = os.path.join(
            self._folder_path,
            self.__PLATFORM_DICT_INV.get(platform, ''),
            FileHelper.retrieve_file_name(rom_file)
        )
        FileHelper.copy_file(
            source_file_path=rom_file,
            destination_file_path=skraper_rom_file
        )

        # Add field for the rom
        fields_to_add[self.__TAG_PATH] = self.__FILE_PREFIX
        fields_to_add[self.__TAG_PATH] += FileHelper.retrieve_file_name(
            rom_file
        )

        # Retrieve better game info depending on a priority
        better_software = None
        better_game_info = None
        for software in self.__SOFTWARE_GAME_INFO_PRIORITY:
            game_info_file = game_info_files.get(software, None)
            if game_info_file is not None:
                better_software = software
                better_game_info = FileHelper.read_file(game_info_file)
                break

        # If no game info found, finish the installation without info and media
        if better_game_info is None:
            return True

        # Install media files
        skraper_media_files = {}
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
            file_name = FileHelper.retrieve_file_basename(skraper_rom_file)
            file_name += FileHelper.retrieve_file_extension(media_file)
            skraper_media_files[media] = os.path.join(
                self._folder_path,
                self.__PLATFORM_DICT_INV.get(platform, ''),
                self.__MEDIA_PATH,
                key,
                file_name
            )
            FileHelper.copy_file(
                source_file_path=media_file,
                destination_file_path=skraper_media_files[media]
            )

            # Add field for the media
            fields_to_add[key] = self.__FILE_PREFIX
            fields_to_add[key] += media_folder
            fields_to_add[key] += self.__PATH_SEPARATOR
            fields_to_add[key] += file_name

        # Normalize lines
        lines = []
        for line in better_game_info.splitlines():
            if self.__FILE_PREFIX in line or line.strip() == "":
                continue
            stripped = line.lstrip()
            if stripped.startswith(f'<{self.__TAG_GAME}') or stripped.startswith(f'</{self.__TAG_GAME}'):
                lines.append(self.__PARENT_PREFIX + stripped)
            else:
                lines.append(self.__CHILD_PREFIX + stripped)

        # Build new tags
        new_tags = [
            f"{self.__CHILD_PREFIX}<{field_key}>{field_value}</{field_key}>"
            for field_key, field_value in fields_to_add.items()
        ]

        # Insert new tags before the last line
        if len(lines) >= 1:
            lines[-1:-1] = new_tags

        better_game_info = "\n".join(lines)

        # Add the game info before </gameList>
        game_list_xml_path = self.__retrieve_game_list_xml_path(
            platform=platform
        )
        game_list_xml_content = FileHelper.read_file(game_list_xml_path)

        if len(game_list_xml_content) == 0:
            # Build an empty XML file if XML doesn't exist
            game_list_xml_content = f"""<?xml version="1.0"?>
<gameList>
{self.__PARENT_PREFIX}<provider>
{self.__CHILD_PREFIX}<System>{platform.value}</System>
{self.__CHILD_PREFIX}<software>{better_software.value}</software>
{self.__PARENT_PREFIX}</provider>
</gameList>
"""

        closing_tag = f"</{self.__TAG_GAMES}>"
        if closing_tag not in game_list_xml_content:
            raise Exception(f'{game_list_xml_path} is inconsistent!')

        game_list_xml_content = game_list_xml_content.replace(
            closing_tag,
            f"{better_game_info}\n{closing_tag}",
            1
        )

        return FileHelper.write_file(
            file_path=game_list_xml_path,
            content=game_list_xml_content
        )
