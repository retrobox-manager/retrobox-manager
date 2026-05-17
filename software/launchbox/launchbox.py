#!/usr/bin/python3
"""Software for the Software LAUNCHBOX"""

import os
import re

from libraries.constants.constants import Component, Constants, Media, SoftwareId
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.xml.xml_helper import XmlHelper
from software.abstract_software import AbstractSoftware

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-positional-arguments


class Launchbox(AbstractSoftware):
    """Software for the Software LAUNCHBOX"""

    __PATH_ROMS = 'roms'
    __PATH_IMAGES = 'Images'

    __TAG_ROOT = 'LaunchBox'
    __TAG_GAME = 'Game'
    __TAG_PATH = 'ApplicationPath'
    __TAG_NAME = 'Title'

    __FILE_PREFIX = '..\\..\\'
    __PATH_SEPARATOR = '\\'

    __PARENT_PREFIX = '  '
    __CHILD_PREFIX = '    '

    __INVALID_CHARS = r'[\\/:*?"<>|]'

    def __retrieve_games_xml_path(
        self,
        platform: str
    ) -> str:
        """Retrieve the path for XML file listing games"""

        return os.path.join(
            self.get_context().path,
            'Data',
            'Platforms',
            f'{self.retrieve_platform_roms_folder(platform=platform)}{Constants.XML_EXTENSION}'
        )

    def __retrieve_platforms_xml_path(
        self
    ) -> str:
        """Retrieve the path for XML file listing platforms"""

        return os.path.join(
            self.get_context().path,
            'Data',
            f'Platforms{Constants.XML_EXTENSION}'
        )

    def __retrieve_parents_xml_path(
        self
    ) -> str:
        """Retrieve the path for XML file listing parents"""

        return os.path.join(
            self.get_context().path,
            'Data',
            f'Parents{Constants.XML_EXTENSION}'
        )

    def __build_game_criteria(self, game_item: dict) -> dict[str, str]:
        """Build criteria to find a game"""

        return {
            self.__TAG_PATH: game_item[Constants.UI_TABLE_KEY_COL_ROM]
        }

    def __retrieve_game_media_name(self, game_item: dict) -> str:
        return re.sub(
            self.__INVALID_CHARS,
            '_',
            FileHelper.retrieve_file_basename(
                game_item[Constants.UI_TABLE_KEY_COL_ROM]
            )
        )

    def get_id(self) -> SoftwareId:
        """Get id"""

        return SoftwareId.LAUNCHBOX

    def list_roms_folders(self) -> list[str]:
        """List folders where a rom can be found"""

        _, folders = FileHelper.list_files_and_folders(
            folder_path=os.path.join(
                self.get_context().path,
                self.__PATH_ROMS
            )
        )

        return folders

    def get_default_platform_associations(self) -> dict[str, str]:
        """Get default platform associations"""

        platform_associations: dict[str, str] = {
            Constants.DEFAULT_PLATFORM_MICROSOFT_XBOX360: 'Microsoft Xbox 360',
            Constants.DEFAULT_PLATFORM_NINTENDO_SWITCH: 'Nintendo Switch',
            Constants.DEFAULT_PLATFORM_NINTENDO_64: 'Nintendo 64',
            Constants.DEFAULT_PLATFORM_NINTENDO_GAMECUBE: 'Nintendo GameCube',
            Constants.DEFAULT_PLATFORM_SEGA_DREAMCAST: 'Sega Dreamcast',
            Constants.DEFAULT_PLATFORM_SEGA_MASTERSYSTEM: 'Sega Master System',
            Constants.DEFAULT_PLATFORM_SEGA_MEGADRIVE: 'Sega Genesis',
            Constants.DEFAULT_PLATFORM_SONY_PLAYSTATION_2: 'Sony Playstation 2',
            Constants.DEFAULT_PLATFORM_ATARI_2600: 'Atari 2600',
            Constants.DEFAULT_PLATFORM_ATARI_7800: 'Atari 7800',
            Constants.DEFAULT_PLATFORM_NINTENDO_GAMEBOY_ADVANCE: 'Nintendo Game Boy Advance',
            Constants.DEFAULT_PLATFORM_SONY_PSP: 'Sony PSP',
            Constants.DEFAULT_PLATFORM_NINTENDO_NES: 'Nintendo Entertainment System',
            Constants.DEFAULT_PLATFORM_NINTENDO_SNES: 'Super Nintendo Entertainment System',
            Constants.DEFAULT_PLATFORM_NINTENDO_WII: 'Nintendo Wii',
            Constants.DEFAULT_PLATFORM_PC: 'Windows',
            Constants.DEFAULT_PLATFORM_SEGA_GAMEGEAR: 'Sega Game Gear'
        }

        return platform_associations

    def get_default_media_associations(self) -> dict[Media, str]:
        """Get default media associations"""

        media_associations: dict[Media, str] = {
            Media.BOX_2D_FRONT: 'Box - Front',
            Media.BOX_2D_SIDE: 'Box - Spine',
            Media.BOX_2D_BACK: 'Box - Back',
            Media.BOX_2D: 'Box - Full',
            Media.BOX_3D: 'Box - 3D',
            Media.SUPPORT: 'Cart - Front',
            Media.LOGO: 'Clear Logo',
            Media.FAN_ART: 'Fanart - Background',
            Media.SCREENSHOT_TITLE: 'Screenshot - Game Title',
            Media.SCREENSHOT_MIX: 'Screenshot - Gameplay',
            Media.MANUAL: 'Manuals',
            Media.VIDEO: 'Videos'
        }

        return media_associations

    def get_default_media_positions(self) -> dict[tuple[int, int], Media]:
        """Get default media positions"""

        media_positions: dict[tuple[int, int], Media] = {
            (0, 0): Media.BOX_2D_FRONT,
            (0, 1): Media.BOX_2D_SIDE,
            (0, 2): Media.BOX_2D_BACK,
            (0, 3): Media.BOX_2D,
            (1, 0): Media.BOX_3D,
            (1, 1): Media.SUPPORT,
            (1, 2): Media.LOGO,
            (1, 3): Media.FAN_ART,
            (2, 0): Media.SCREENSHOT_TITLE,
            (2, 1): Media.SCREENSHOT_MIX,
            (2, 2): Media.MANUAL,
            (2, 3): Media.VIDEO
        }

        return media_positions

    def list_media_resources(self) -> list[str]:
        """List media resources"""

        return [
            'Box - Front',
            'Box - Spine',
            'Box - Back',
            'Box - Full',
            'Box - 3D',
            'Cart - Front',
            'Clear Logo',
            'Fanart - Background',
            'Screenshot - Game Title',
            'Screenshot - Gameplay',
            'Manuals',
            'Videos'
        ]

    def list_games_with_rom(self, platform: str) -> dict[str, str]:
        """List games in a dictionary where the key is the rom and the value is the name"""

        # Initialize result
        result: dict[str, str] = {}

        # Retrieve game list XML path from platform
        games_xml_path = self.__retrieve_games_xml_path(
            platform=platform
        )

        # Add games for the platform
        if FileHelper.is_file_exists(games_xml_path):
            # Retrieve tags values
            tag_path_values = XmlHelper.list_tag_values(
                xml_file_path=games_xml_path,
                parent_tag=self.__TAG_GAME,
                tag=self.__TAG_PATH
            )
            tag_name_values = XmlHelper.list_tag_values(
                xml_file_path=games_xml_path,
                parent_tag=self.__TAG_GAME,
                tag=self.__TAG_NAME
            )

            # Error if BDD inconsistent
            if len(tag_name_values) != len(tag_name_values):
                raise Exception(f'{games_xml_path} is inconsistent!')

            for rom_relative_path in tag_path_values:
                # Check if the rom file exists
                rom_file = FileHelper.retrieve_absolute_path(
                    folder_path=self.get_context().path,
                    relative_path=rom_relative_path
                )
                if FileHelper.is_file_exists(rom_file):
                    result[FileHelper.retrieve_file_name(rom_file)] = tag_name_values[
                        tag_path_values.index(rom_relative_path)
                    ]

        return result

    def retrieve_media_files(self, platform: str, game_item: dict) -> dict[Media, str]:
        """Retrieve media files"""

        # Initialize result
        result: dict[Media, str] = {}

        # Add media for the game
        for media, resource in self.get_context().media_associations.items():

            # Retrieve media folder path
            if media in [Media.VIDEO, Media.MANUAL]:
                media_folder_path = os.path.join(
                    self.get_context().path,
                    resource,
                    self.get_context().platform_associations[platform]
                )
            else:
                media_folder_path = os.path.join(
                    self.get_context().path,
                    self.__PATH_IMAGES,
                    self.get_context().platform_associations[platform],
                    resource
                )

            # Retrieve media name
            media_name = self.__retrieve_game_media_name(
                game_item=game_item
            )
            if media not in [Media.MANUAL]:
                media_name += '-01'

            for relative_path in FileHelper.list_relative_paths(
                folder_path=media_folder_path,
                file_name=media_name,
                error_if_not_found=False
            ):
                result[media] = os.path.join(
                    media_folder_path,
                    relative_path
                )

        return result

    def retrieve_rom_file(self, platform: str, game_item: dict) -> str:
        """Retrieve rom file"""

        # Initialize result
        result = None

        # Get game data
        game_data = XmlHelper.get_tag_data(
            xml_file_path=self.__retrieve_games_xml_path(
                platform=platform
            ),
            parent_tag=self.__TAG_ROOT,
            tag=self.__TAG_GAME,
            criteria=self.__build_game_criteria(game_item)
        )

        if game_data is None or len(game_data) == 0:
            return result

        # Retrieve rom file
        rom_file = FileHelper.retrieve_absolute_path(
            folder_path=self.get_context().path,
            relative_path=game_data[self.__TAG_PATH]
        )

        # Check that rom file exists
        if not FileHelper.is_file_exists(rom_file):
            return result

        result = rom_file

        return result

    def retrieve_software_game_info_path(
        self,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve Software game's info path"""

        # For this software, the game information path depends only on the platform
        return self.__retrieve_games_xml_path(
            platform=platform
        )

    def retrieve_game_info(
        self,
        game_info_path: str,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve game info"""

        # Initialize result
        result = ''

        # Game data if the game info path if from retrobox manager
        if str(game_info_path).startswith(
            str(Context.get_games_path())
        ):
            return FileHelper.read_file(
                file_path=game_info_path
            )

        # Get game data
        game_data = XmlHelper.get_tag_content(
            xml_file_path=game_info_path,
            parent_tag=self.__TAG_ROOT,
            tag=self.__TAG_GAME,
            criteria=self.__build_game_criteria(game_item)
        )

        if game_data is None or len(game_data) == 0:
            return result

        # Filter out lines containing the file prefix
        lines = [
            line for line in game_data.splitlines()
            if self.__TAG_PATH not in line and line.strip() != ""
        ]

        result = '\n'.join(lines)

        return result

    def retrieve_game_name(
        self,
        game_info_path: str,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve game's name"""

        # Retrieve game info
        game_info = self.retrieve_game_info(
            game_info_path=game_info_path,
            platform=platform,
            game_item=game_item
        )

        # Extract the name from game info
        name = re.search(
            r"<Title>(.*?)</Title>",
            game_info, re.DOTALL
        )
        if name is None:
            name = ''
        else:
            name = name.group(1)

        return name

    def retrieve_game_description(
        self,
        game_info_path: str,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve game's description"""

        # Retrieve game info
        game_info = self.retrieve_game_info(
            game_info_path=game_info_path,
            platform=platform,
            game_item=game_item
        )

        # Extract the description from game info
        description = re.search(
            r"<Notes>(.*?)</Notes>",
            game_info, re.DOTALL
        )
        if description is None:
            description = ''
        else:
            description = description.group(1)

        return description

    def uninstall_game(
        self,
        platform: str,
        game_item: dict
    ) -> bool:
        """Uninstall game"""

        # Delete media files
        if Component.MEDIA in Context.get_selected_components():
            media_files = self.retrieve_media_files(
                platform=platform,
                game_item=game_item
            )
            for media_file in media_files.values():
                FileHelper.delete_file(
                    file_path=media_file
                )

        # Delete rom file
        if Component.ROM in Context.get_selected_components():
            rom_file_path = self.retrieve_rom_file(
                platform=platform,
                game_item=game_item
            )

            # Delete included rom files
            for included_rom_file in FileHelper.get_included_files(
                file_path=rom_file_path
            ):
                FileHelper.delete_file(
                    file_path=included_rom_file
                )

            FileHelper.delete_file(
                file_path=rom_file_path
            )

            XmlHelper.delete_tag(
                xml_file_path=self.__retrieve_games_xml_path(
                    platform=platform
                ),
                parent_tag=self.__TAG_ROOT,
                tag=self.__TAG_GAME,
                criteria=self.__build_game_criteria(game_item)
            )

        return True

    def install_game(
        self,
        platform: str,
        game_item: dict,
        media_files: dict[Media, str],
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

        # Retrieve platform path
        platform_path = self.get_context().platform_associations[platform]

        # Retrieve rom file
        launchbox_rom_file = os.path.join(
            self.get_context().path,
            self.__PATH_ROMS,
            platform_path,
            FileHelper.retrieve_file_name(rom_file)
        )

        # Copy the rom
        if Component.ROM in Context.get_selected_components():
            FileHelper.copy_file(
                source_file_path=rom_file,
                destination_file_path=launchbox_rom_file
            )

            # Copy included rom files
            source_included_rom_files = FileHelper.get_included_files(
                file_path=rom_file
            )
            destination_included_rom_files = FileHelper.get_included_files(
                file_path=launchbox_rom_file
            )
            for source_path, destination_path in zip(
                source_included_rom_files,
                destination_included_rom_files
            ):
                FileHelper.copy_file(
                    source_file_path=source_path,
                    destination_file_path=destination_path
                )

        # Add field for the rom
        fields_to_add[self.__TAG_PATH] = self.__PATH_ROMS
        fields_to_add[self.__TAG_PATH] += self.__PATH_SEPARATOR
        fields_to_add[self.__TAG_PATH] += platform_path
        fields_to_add[self.__TAG_PATH] += self.__PATH_SEPARATOR
        fields_to_add[self.__TAG_PATH] += FileHelper.retrieve_file_name(
            rom_file
        )

        # Retrieve game info file path prioritizing the game info source
        game_info_software = self.get_registered_software(
            software_id=self.retrieve_retrobox_manager_game_info_software_id(
                platform=platform,
                game_item=game_item
            )
        )
        game_info_path = game_info_software.retrieve_retrobox_manager_game_info_path(
            platform=platform,
            game_item=game_item
        )

        # If no game info found, stop the installation
        if game_info_path is None:
            return True

        # Retrieve game's name and game's description
        game_name = game_info_software.retrieve_game_name(
            game_info_path=game_info_path,
            platform=platform,
            game_item=game_item
        )
        game_description = game_info_software.retrieve_game_description(
            game_info_path=game_info_path,
            platform=platform,
            game_item=game_item
        )

        # Build game info
        game_info = f"""  <Game>
    <Title>{game_name}</Title>
    <Notes>{game_description}</Notes>
    <Platform>{platform_path}</Platform>
  </Game>"""

        # Install media files
        for media, resource in self.get_context().media_associations.items():
            media_file = media_files.get(
                media, None
            )
            if media_file is None:
                continue

            # Retrieve media folder path
            if media in [Media.VIDEO, Media.MANUAL]:
                media_folder_path = os.path.join(
                    self.get_context().path,
                    resource,
                    platform_path
                )
            else:
                media_folder_path = os.path.join(
                    self.get_context().path,
                    self.__PATH_IMAGES,
                    platform_path,
                    resource
                )

            # Retrieve media name
            media_name = self.__retrieve_game_media_name(
                game_item=game_item
            )
            if media not in [Media.MANUAL]:
                media_name += '-01'
            media_name += FileHelper.retrieve_file_extension(media_file)

            # Copy media file in software
            if Component.MEDIA in Context.get_selected_components():
                FileHelper.copy_file(
                    source_file_path=media_file,
                    destination_file_path=os.path.join(
                        media_folder_path,
                        media_name
                    )
                )

        # Normalize lines
        lines = []
        lines.append(f'{self.__PARENT_PREFIX}<{self.__TAG_GAME}>')
        for line in game_info.splitlines()[1:-1]:
            if self.__FILE_PREFIX in line or line.strip() == "":
                continue
            stripped = line.lstrip()
            lines.append(self.__CHILD_PREFIX + stripped)
        lines.append(f'{self.__PARENT_PREFIX}</{self.__TAG_GAME}>')

        # Build new tags
        new_tags = [
            f"{self.__CHILD_PREFIX}<{field_key}>{field_value}</{field_key}>"
            for field_key, field_value in fields_to_add.items()
        ]

        # Insert new tags before the last line
        if len(lines) >= 1:
            lines[-1:-1] = new_tags

        game_info = "\n".join(lines)

        # Add the game info before </gameList>
        games_xml_path = self.__retrieve_games_xml_path(
            platform=platform
        )
        games_xml_content = FileHelper.read_file(games_xml_path)

        if len(games_xml_content) == 0:
            # Build an empty XML file if XML doesn't exist
            games_xml_content = f"""<?xml version="1.0"?>
<{self.__TAG_ROOT}>
</{self.__TAG_ROOT}>
"""

            # Add the platform
            new_platform = f"""
  <Platform>
    <Name>{platform_path}</Name>
    <Folder>{self.__PATH_ROMS}{self.__PATH_SEPARATOR}{platform_path}</Folder>
  </Platform>"""
            platforms_xml_path = self.__retrieve_platforms_xml_path()
            platforms_xml_content = FileHelper.read_file(
                platforms_xml_path
            )
            starting_tag = f"<{self.__TAG_ROOT}>"
            if starting_tag not in platforms_xml_content:
                raise Exception(
                    f'{platforms_xml_content} is inconsistent!'
                )
            platforms_xml_content = platforms_xml_content.replace(
                starting_tag,
                f"{starting_tag}{new_platform}",
                1
            )
            FileHelper.write_file(
                file_path=platforms_xml_path,
                content=platforms_xml_content
            )

            # Add the parent
            new_parent = f"""
  <Parent>
    <PlatformName>{platform_path}</PlatformName>
    <PlaylistId />
    <PlatformCategoryName />
    <ParentPlatformName />
    <ParentPlaylistId />
    <ParentPlatformCategoryName>Consoles</ParentPlatformCategoryName>
  </Parent>"""
            parents_xml_path = self.__retrieve_parents_xml_path()
            parents_xml_content = FileHelper.read_file(
                parents_xml_path
            )
            starting_tag = f"<{self.__TAG_ROOT}>"
            if starting_tag not in parents_xml_content:
                raise Exception(
                    f'{parents_xml_content} is inconsistent!'
                )
            parents_xml_content = parents_xml_content.replace(
                starting_tag,
                f"{starting_tag}{new_parent}",
                1
            )
            FileHelper.write_file(
                file_path=parents_xml_path,
                content=parents_xml_content
            )

        closing_tag = f"</{self.__TAG_ROOT}>"
        if closing_tag not in games_xml_content:
            raise Exception(f'{games_xml_path} is inconsistent!')

        games_xml_content = games_xml_content.replace(
            closing_tag,
            f"{game_info}\n{closing_tag}",
            1
        )

        FileHelper.write_file(
            file_path=games_xml_path,
            content=games_xml_content
        )

        return True
