#!/usr/bin/python3
"""Software for the Software EMU_MOVIES"""

import os
from libraries.constants.constants import Component, Constants, Media, SoftwareId
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from software.abstract_software import AbstractSoftware

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


class EmuMovies(AbstractSoftware):
    """Software for the Software EMU_MOVIES"""

    __PATH_ROMS = 'roms'
    __PATH_MEDIA = 'media'

    def get_id(self) -> SoftwareId:
        """Get id"""

        return SoftwareId.EMU_MOVIES

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
            Constants.DEFAULT_PLATFORM_MICROSOFT_XBOX360: 'Microsoft_Xbox_360',
            Constants.DEFAULT_PLATFORM_NINTENDO_64: 'Nintendo_64DD',
            Constants.DEFAULT_PLATFORM_NINTENDO_GAMECUBE: 'Nintendo_GameCube',
            Constants.DEFAULT_PLATFORM_SEGA_DREAMCAST: 'Sega_Dreamcast',
            Constants.DEFAULT_PLATFORM_SEGA_MASTERSYSTEM: 'Sega_Master_System',
            Constants.DEFAULT_PLATFORM_SEGA_MEGADRIVE: 'Sega_Genesis',
            Constants.DEFAULT_PLATFORM_SONY_PLAYSTATION_2: 'Sony_Playstation_2',
            Constants.DEFAULT_PLATFORM_NINTENDO_SWITCH: 'Nintendo_Switch',
            Constants.DEFAULT_PLATFORM_ATARI_2600: 'Atari_2600',
            Constants.DEFAULT_PLATFORM_ATARI_7800: 'Atari_7800',
            Constants.DEFAULT_PLATFORM_NINTENDO_GAMEBOY_ADVANCE: 'Nintendo_Game_Boy_Advance',
            Constants.DEFAULT_PLATFORM_SNK_NEOGEO: 'SNK_Neo_Geo_AES',
            Constants.DEFAULT_PLATFORM_SONY_PSP: 'Sony_PSP',
            Constants.DEFAULT_PLATFORM_NINTENDO_NES: 'Nintendo_NES',
            Constants.DEFAULT_PLATFORM_NINTENDO_SNES: 'Nintendo_SNES',
            Constants.DEFAULT_PLATFORM_NINTENDO_WII: 'Nintendo_Wii',
            Constants.DEFAULT_PLATFORM_SEGA_GAMEGEAR: 'Sega_Game_Gear'
        }

        return platform_associations

    def get_default_media_associations(self) -> dict[Media, str]:
        """Get default media associations"""

        media_associations: dict[Media, str] = {
            Media.VIDEO: 'Video_MP4_HI_QUAL'
        }

        return media_associations

    def get_default_media_positions(self) -> dict[tuple[int, int], Media]:
        """Get default media positions"""

        media_positions: dict[tuple[int, int], Media] = {
            (2, 2): Media.VIDEO
        }

        return media_positions

    def list_media_resources(self) -> list[str]:
        """List media resources"""

        return [
            'Video_MP4_HI_QUAL'
        ]

    def list_games_with_rom(self, platform: str) -> dict[str, str]:
        """List games in a dictionary where the key is the rom and the value is the name"""

        # Initialize result
        result: dict[str, str] = {}

        # Retrieve folder path
        folder_path = os.path.join(
            self.get_context().path,
            self.__PATH_ROMS,
            self.retrieve_platform_roms_folder(platform=platform)
        )

        # List roms relative paths
        roms_relative_paths = FileHelper.list_relative_paths(
            folder_path=folder_path,
            file_name='*',
            error_if_not_found=False
        )

        # Define relative paths to exclude (included files)
        relative_paths_to_exclude = []
        for rom_relative_path in roms_relative_paths:
            for included_file in FileHelper.get_included_files(
                file_path=os.path.join(
                    self.get_context().path,
                    self.__PATH_ROMS,
                    self.retrieve_platform_roms_folder(platform=platform),
                    rom_relative_path
                )
            ):
                relative_paths_to_exclude.append(
                    FileHelper.retrieve_relative_path(
                        folder_path=folder_path,
                        file_path=included_file
                    )
                )

        # Add games for the platform
        for rom_relative_path in roms_relative_paths:
            # Do nothing if relative path to exclude
            if rom_relative_path in relative_paths_to_exclude:
                continue

            result[rom_relative_path] = FileHelper.retrieve_file_basename(
                file_path=rom_relative_path
            )

        return result

    def retrieve_media_files(self, platform: str, game_item: dict) -> dict[Media, str]:
        """Retrieve media files"""

        # Initialize result
        result: dict[Media, str] = {}

        # Retrieve media's path
        media_path = os.path.join(
            self.get_context().path,
            self.__PATH_MEDIA,
            self.retrieve_platform_roms_folder(platform=platform)
        )

        # Add media for the game
        for folder in FileHelper.list_sub_directories(
            folder_path=media_path
        ):
            media = self.retrieve_media(resource=folder)
            if media is None:
                continue

            relative_paths = FileHelper.list_relative_paths(
                folder_path=os.path.join(
                    media_path,
                    folder
                ),
                file_name=FileHelper.retrieve_file_basename(
                    game_item[Constants.UI_TABLE_KEY_COL_ROM]
                ),
                error_if_not_found=False
            )

            if len(relative_paths) == 1:
                result[media] = os.path.join(
                    media_path,
                    folder,
                    relative_paths[0]
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
            self.retrieve_platform_roms_folder(platform=platform),
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

        # No game info file for this software
        return None

    def retrieve_game_info(
        self,
        game_info_path: str,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve game info"""

        # Game data if the game info path if from retrobox manager
        if str(game_info_path).startswith(
            str(Context.get_games_path())
        ):
            return FileHelper.read_file(
                file_path=game_info_path
            )

        # Get game data
        info = f'platform: {platform}'
        info += '\n'
        info += f'name: {game_item[Constants.UI_TABLE_KEY_COL_NAME]}'
        info += '\n'
        info += f'rom: {game_item[Constants.UI_TABLE_KEY_COL_ROM]}'

        return info

    def retrieve_game_name(
        self,
        game_info_path: str,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve game's name"""

        return game_item[Constants.UI_TABLE_KEY_COL_NAME]

    def retrieve_game_description(
        self,
        game_info_path: str,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve game's description"""

        return game_item[Constants.UI_TABLE_KEY_COL_NAME]

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

            # Delete rom file
            FileHelper.delete_file(
                file_path=os.path.join(
                    self.get_context().path,
                    self.__PATH_ROMS,
                    self.retrieve_platform_roms_folder(platform=platform),
                    game_item[Constants.UI_TABLE_KEY_COL_ROM]
                )
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

        # Retrieve rom file
        emumovies_rom_file = os.path.join(
            self.get_context().path,
            self.__PATH_ROMS,
            self.get_context().platform_associations[platform],
            FileHelper.retrieve_file_name(rom_file)
        )

        # Copy the rom
        if Component.ROM in Context.get_selected_components():
            FileHelper.copy_file(
                source_file_path=rom_file,
                destination_file_path=emumovies_rom_file
            )

        # Install media files
        if Component.MEDIA in Context.get_selected_components():
            for media, resource in self.get_context().media_associations.items():
                media_file = media_files.get(media, None)
                if media_file is None:
                    continue

                # Copy media file in software
                file_name = FileHelper.retrieve_file_basename(
                    emumovies_rom_file)
                file_name += FileHelper.retrieve_file_extension(media_file)
                FileHelper.copy_file(
                    source_file_path=media_file,
                    destination_file_path=os.path.join(
                        self.get_context().path,
                        self.__PATH_MEDIA,
                        self.get_context().platform_associations[platform],
                        resource,
                        file_name
                    )
                )

        return True
