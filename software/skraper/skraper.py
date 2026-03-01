#!/usr/bin/python3
"""Software for the Software SKRAPER"""

import re
import os
from libraries.constants.constants import Component, Constants, Media, SoftwareId
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.xml.xml_helper import XmlHelper
from software.abstract_software import AbstractSoftware

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements


class Skraper(AbstractSoftware):
    """Software for the Software SKRAPER"""

    __TAG_GAMES = 'gameList'
    __TAG_GAME = 'game'
    __TAG_NAME = 'name'
    __TAG_PATH = 'path'

    __PATH_MEDIA = 'media'
    __PATH_ROMS = 'roms'

    __FILE_PREFIX = './'
    __PATH_SEPARATOR = '/'

    __PARENT_PREFIX = '  '
    __CHILD_PREFIX = '    '

    def __retrieve_games_xml_path(
        self,
        platform: str
    ) -> str:
        """Retrieve the path for XML file listing games"""

        return os.path.join(
            self.get_context().path,
            self.__PATH_ROMS,
            self.retrieve_platform_roms_folder(platform=platform),
            f'gamelist{Constants.XML_EXTENSION}'
        )

    def __build_game_criteria(self, game_item: dict) -> dict[str, str]:
        """Build criteria to find a game"""

        return {
            self.__TAG_PATH: game_item[Constants.UI_TABLE_KEY_COL_ROM]
        }

    def get_id(self) -> SoftwareId:
        """Get id"""

        return SoftwareId.SKRAPER

    def list_roms_folders(self) -> list[str]:
        """List folders where a rom can be found"""

        return FileHelper.list_sub_directories(
            folder_path=os.path.join(
                self.get_context().path,
                self.__PATH_ROMS
            )
        )

    def get_default_platform_associations(self) -> dict[str, str]:
        """Get default platform associations"""

        platform_associations: dict[str, str] = {
            Constants.DEFAULT_PLATFORM_NINTENDO_64: 'n64',
            Constants.DEFAULT_PLATFORM_NINTENDO_GAMECUBE: 'gamecube',
            Constants.DEFAULT_PLATFORM_SEGA_DREAMCAST: 'dreamcast',
            Constants.DEFAULT_PLATFORM_SEGA_MASTERSYSTEM: 'mastersystem',
            Constants.DEFAULT_PLATFORM_SEGA_MEGADRIVE: 'megadrive',
            Constants.DEFAULT_PLATFORM_SONY_PLAYSTATION_2: 'ps2',
            Constants.DEFAULT_PLATFORM_ATARI_2600: 'atari2600',
            Constants.DEFAULT_PLATFORM_ATARI_7800: 'atari7800',
            Constants.DEFAULT_PLATFORM_NINTENDO_GAMEBOY_ADVANCE: 'gba',
            Constants.DEFAULT_PLATFORM_SNK_NEOGEO: 'neogeo',
            Constants.DEFAULT_PLATFORM_SONY_PSP: 'psp',
            Constants.DEFAULT_PLATFORM_NINTENDO_NES: 'nes',
            Constants.DEFAULT_PLATFORM_NINTENDO_SNES: 'snes',
            Constants.DEFAULT_PLATFORM_NINTENDO_WII: 'wii',
            Constants.DEFAULT_PLATFORM_SEGA_GAMEGEAR: 'gamegear',
            Constants.DEFAULT_PLATFORM_NINTENDO_SWITCH: 'switch',
            Constants.DEFAULT_PLATFORM_MICROSOFT_XBOX360: 'xbox360'
        }

        return platform_associations

    def get_default_media_associations(self) -> dict[Media, str]:
        """Get default media associations"""

        media_associations: dict[Media, str] = {
            Media.BOX_2D_FRONT: 'box2dfront',
            Media.BOX_2D_SIDE: 'box2dside',
            Media.BOX_2D_BACK: 'box2dback',
            Media.BOX_3D: 'box3d',
            Media.BOX_2D: 'boxtexture',
            Media.SUPPORT: 'support',
            Media.LOGO: 'wheel',
            Media.LOGO_CARBON: 'wheelcarbon',
            Media.LOGO_STEEL: 'wheelsteel',
            Media.SCREENSHOT_GAME: 'screenshot',
            Media.SCREENSHOT_TITLE: 'screenshottitle',
            Media.FAN_ART: 'fanart',
            Media.SCREENSHOT_MIX: 'images',
            Media.MANUAL: 'manuals',
            Media.VIDEO: 'videos'
        }

        return media_associations

    def get_default_media_positions(self) -> dict[tuple[int, int], Media]:
        """Get default media positions"""

        media_positions: dict[tuple[int, int], Media] = {
            (0, 0): Media.BOX_2D_FRONT,
            (0, 1): Media.BOX_2D_SIDE,
            (0, 2): Media.BOX_2D_BACK,
            (0, 3): Media.BOX_3D,
            (1, 0): Media.BOX_2D,
            (1, 1): Media.SUPPORT,
            (1, 2): Media.LOGO,
            (1, 3): Media.LOGO_CARBON,
            (2, 0): Media.LOGO_STEEL,
            (2, 1): Media.SCREENSHOT_GAME,
            (2, 2): Media.SCREENSHOT_TITLE,
            (2, 3): Media.FAN_ART,
            (3, 0): Media.SCREENSHOT_MIX,
            (3, 1): Media.MANUAL,
            (3, 2): Media.VIDEO
        }

        return media_positions

    def list_media_resources(self) -> list[str]:
        """List media resources"""

        return [
            'box2dfront',
            'box2dside',
            'box2dback',
            'box3d',
            'boxtexture',
            'support',
            'supporttexture',
            'wheel',
            'wheelcarbon',
            'wheelsteel',
            'steamgrid',
            'screenmarquee',
            'screenmarqueesmall',
            'marquee',
            'screenshot',
            'screenshottitle',
            'fanart',
            'mix',
            'images',
            'manuals',
            'videos'
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

            for rom_path in tag_path_values:
                # Check if the rom file exists
                rom_file = os.path.join(
                    self.get_context().path,
                    self.__PATH_ROMS,
                    self.get_context().platform_associations[platform],
                    rom_path
                )
                if FileHelper.is_file_exists(rom_file):
                    result[FileHelper.retrieve_file_name(rom_file)] = tag_name_values[
                        tag_path_values.index(rom_path)
                    ]
        else:
            # List roms
            for rom_file in FileHelper.list_relative_paths(
                folder_path=os.path.join(
                    self.get_context().path,
                    self.__PATH_ROMS,
                    self.retrieve_platform_roms_folder(platform=platform)
                ),
                file_name='*'
            ):
                result[rom_file] = FileHelper.retrieve_file_basename(
                    file_path=rom_file
                )

        return result

    def retrieve_media_files(self, platform: str, game_item: dict) -> dict[Media, str]:
        """Retrieve media files"""

        # Initialize result
        result: dict[Media, str] = {}

        # Retrieve media's path
        media_path = os.path.join(
            self.get_context().path,
            self.__PATH_ROMS,
            self.get_context().platform_associations[platform],
            self.__PATH_MEDIA
        )

        # Add media for the game
        for folder in FileHelper.list_sub_directories(
            folder_path=media_path
        ):
            media = self.retrieve_media(resource=folder)
            if media is None:
                continue

            relative_path = FileHelper.get_main_file(
                files_paths=FileHelper.list_relative_paths(
                    folder_path=os.path.join(
                        media_path,
                        folder
                    ),
                    file_name=FileHelper.retrieve_file_basename(
                        game_item[Constants.UI_TABLE_KEY_COL_ROM]
                    ),
                    error_if_not_found=False
                )
            )

            if relative_path is None:
                continue

            result[media] = os.path.join(
                media_path,
                folder,
                relative_path
            )

        return result

    def retrieve_rom_file(self, platform: str, game_item: dict) -> str:
        """Retrieve rom file"""

        # Initialize result
        result = None

        # Retrieve rom file
        rom_file = os.path.join(
            self.get_context().path,
            self.__PATH_ROMS,
            self.get_context().platform_associations[platform],
            game_item[Constants.UI_TABLE_KEY_COL_ROM]
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
            parent_tag=self.__TAG_GAMES,
            tag=self.__TAG_GAME,
            criteria=self.__build_game_criteria(game_item)
        )

        if game_data is None or len(game_data) == 0:
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
            r"<name>(.*?)</name>",
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
            r"<desc>(.*?)</desc>",
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
                parent_tag=self.__TAG_GAMES,
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

        # Retrieve rom file
        skraper_rom_file = os.path.join(
            self.get_context().path,
            self.__PATH_ROMS,
            self.get_context().platform_associations[platform],
            FileHelper.retrieve_file_name(rom_file)
        )

        # Copy the rom
        if Component.ROM in Context.get_selected_components():
            FileHelper.copy_file(
                source_file_path=rom_file,
                destination_file_path=skraper_rom_file
            )

            # Copy included rom files
            source_included_rom_files = FileHelper.get_included_files(
                file_path=rom_file
            )
            destination_included_rom_files = FileHelper.get_included_files(
                file_path=skraper_rom_file
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
        fields_to_add[self.__TAG_PATH] = self.__FILE_PREFIX
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

        # Install media files
        skraper_media_files = {}
        for media, resource in self.get_context().media_associations.items():
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
                self.get_context().path,
                self.__PATH_ROMS,
                self.get_context().platform_associations[platform],
                self.__PATH_MEDIA,
                resource,
                file_name
            )

            if Component.MEDIA in Context.get_selected_components():
                FileHelper.copy_file(
                    source_file_path=media_file,
                    destination_file_path=skraper_media_files[media]
                )

            # Add field for the media
            fields_to_add[resource] = self.__FILE_PREFIX
            fields_to_add[resource] += media_folder
            fields_to_add[resource] += self.__PATH_SEPARATOR
            fields_to_add[resource] += file_name

        # Normalize lines
        lines = []
        for line in FileHelper.read_file(
            file_path=game_info_path
        ).splitlines():
            if self.__FILE_PREFIX in line or line.strip() == "":
                continue
            stripped = line.lstrip()
            if stripped.startswith(f'<{self.__TAG_GAME}') or \
                    stripped.startswith(f'</{self.__TAG_GAME}'):
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

        game_info = "\n".join(lines)

        # Add the game info before </gameList>
        games_xml_path = self.__retrieve_games_xml_path(
            platform=platform
        )
        games_xml_content = FileHelper.read_file(games_xml_path)

        if len(games_xml_content) == 0:
            # Build an empty XML file if XML doesn't exist
            games_xml_content = f"""<?xml version="1.0"?>
<gameList>
{self.__PARENT_PREFIX}<provider>
{self.__CHILD_PREFIX}<System>{platform}</System>
{self.__CHILD_PREFIX}<software>{self.get_id()}</software>
{self.__PARENT_PREFIX}</provider>
</gameList>
"""

        closing_tag = f"</{self.__TAG_GAMES}>"
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
