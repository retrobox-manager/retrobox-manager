#!/usr/bin/python3
"""Executor to export Games"""

import os
from tkinter import messagebox
from executor.games.abstract_games_executor import AbstractGamesExecutor
from libraries.constants.constants import Action, Category, Component, Constants
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper


class ExportGamesExecutor(AbstractGamesExecutor):
    """Executor to export Games"""

    # Constants for replacements
    __GAME_INFO_REPLACEMENTS = {
        '&amp;': 'And',
        '&': 'And'
    }
    __ROM_REPLACEMENTS = {
        '&': 'And'
    }
    __ROM_RSTRIPS = [
        '.'
    ]

    def __init__(
        self,
        sub_items_enabled: bool = False
    ):
        """Initialize executor"""

        super().__init__(
            sub_items_enabled=sub_items_enabled
        )

        self.__only_add_data = False

    def get_action(self) -> Action:
        """Get Action"""

        return Action.EXPORT

    # pylint: disable=unused-argument
    def confirm_execution(self, parent: any) -> True:
        """Confirm for execution"""

        platforms: list[str] = []
        if Context.get_selected_category() == Category.GAMES:
            platforms.append(Context.get_selected_platform())
        else:
            for item in Context.get_selected_rows():
                platforms.append(item[Constants.UI_TABLE_KEY_COL_ID])

        # If platform already existing ask if only_add
        for platform in platforms:
            if FileHelper.is_folder_exists(
                folder_path=os.path.join(
                    Context.get_games_path(),
                    platform
                )
            ):
                self.__only_add_data = messagebox.askyesno(
                    Context.get_text('question'),
                    Context.get_text(
                        'question_only_add_data'
                    ),
                    parent=parent
                )

                return True

        # No confirmation by default
        return True

    @staticmethod
    def retrieve_game_folder(item: dict) -> str:
        """Retrieve game's folder from specified item"""

        result = item[Constants.UI_TABLE_KEY_COL_ID]
        for rom_strip in ExportGamesExecutor.__ROM_RSTRIPS:
            result = result.rstrip(
                rom_strip
            )
        for replace_from, replace_to in ExportGamesExecutor.__ROM_REPLACEMENTS.items():
            result = result.replace(replace_from, replace_to)
        return result

    @staticmethod
    def retrieve_rom_path(item: dict) -> str:
        """Retrieve rom's path from specified item and rom_file"""

        result = ExportGamesExecutor.retrieve_game_folder(
            item=item
        )
        result += FileHelper.retrieve_file_extension(
            file_path=item[Constants.UI_TABLE_KEY_COL_ROM]
        )
        return result

    def list_sub_items(self, item: dict) -> list[dict]:
        """List sub items for the current item"""

        # Initialize result
        result: list[dict] = []

        # Select the platform
        Context.set_selected_platform(
            platform=item[Constants.UI_TABLE_KEY_COL_ID]
        )

        # List games with rom for selected Software and selected Platform
        for rom, game_name in self._software.list_games_with_rom(
            platform=Context.get_selected_platform()
        ).items():

            # Build sub item
            sub_item = {}
            sub_item[Constants.UI_TABLE_KEY_COL_ID] = FileHelper.retrieve_file_basename(
                rom
            )
            sub_item[Constants.UI_TABLE_KEY_COL_NAME] = game_name
            sub_item[Constants.UI_TABLE_KEY_COL_ROM] = rom

            # Add sub item
            result.append(sub_item)

        return result

    def do_execution(self, item: dict):
        """Do execution for an item"""

        # Copy files for media
        if Component.MEDIA in Context.get_selected_components():
            for media, file_path in self._software.retrieve_media_files(
                platform=Context.get_selected_platform(),
                game_item=item
            ).items():
                # Retrieve destination's file
                destination_file_path = os.path.join(
                    Context.get_games_path(),
                    Context.get_selected_platform(),
                    self.retrieve_game_folder(
                        item=item
                    ),
                    Constants.PATH_MEDIA,
                    f'{media.name.lower()}{FileHelper.retrieve_file_extension(
                        file_path=file_path
                    )}'
                )

                if not self.__only_add_data or not FileHelper.is_file_exists(
                    file_path=destination_file_path
                ):
                    # Delete files with the same basename
                    FileHelper.delete_file(
                        file_path=destination_file_path,
                        delete_all_extensions=True
                    )

                    # Copy file in destination's folder
                    FileHelper.copy_file(
                        source_file_path=file_path,
                        destination_file_path=destination_file_path
                    )

        # Copy rom
        if Component.ROM in Context.get_selected_components():
            rom_file = self._software.retrieve_rom_file(
                platform=Context.get_selected_platform(),
                game_item=item
            )
            if rom_file is not None or FileHelper.is_file_exists(
                file_path=rom_file
            ):
                # Retrieve rom folder
                rom_folder_path = os.path.join(
                    Context.get_games_path(),
                    Context.get_selected_platform(),
                    self.retrieve_game_folder(
                        item=item
                    ),
                    Constants.PATH_ROM
                )

                if not self.__only_add_data or not FileHelper.is_folder_exists(
                    folder_path=rom_folder_path
                ):
                    # Retrieve destination's file
                    destination_file_path = os.path.join(
                        rom_folder_path,
                        self.retrieve_rom_path(
                            item=item
                        )
                    )

                    # Delete files with the same basename
                    FileHelper.delete_file(
                        file_path=destination_file_path,
                        delete_all_extensions=True
                    )

                    # Copy file in destination's folder
                    FileHelper.copy_file(
                        source_file_path=rom_file,
                        destination_file_path=destination_file_path
                    )

                    # Copy included rom files
                    for included_rom_file in FileHelper.get_included_files(
                        file_path=rom_file
                    ):
                        # Retrieve destination's file
                        destination_file_path = os.path.join(
                            rom_folder_path,
                            FileHelper.retrieve_file_name(
                                file_path=included_rom_file
                            )
                        )

                        # Delete files if existing
                        FileHelper.delete_file(
                            file_path=destination_file_path
                        )

                        # Copy file in destination's folder
                        FileHelper.copy_file(
                            source_file_path=included_rom_file,
                            destination_file_path=destination_file_path
                        )

        # Retrieve game's info
        if Component.INFO in Context.get_selected_components():
            game_info = self._software.retrieve_game_info(
                game_info_path=self._software.retrieve_software_game_info_path(
                    platform=Context.get_selected_platform(),
                    game_item=item
                ),
                platform=Context.get_selected_platform(),
                game_item=item
            )

            # Do replacements in game info
            for replace_from, replace_to in self.__GAME_INFO_REPLACEMENTS.items():
                game_info = game_info.replace(replace_from, replace_to)

            # If no game info found, finish the export
            if len(game_info) == 0:
                return

            xml_file_path = os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform(),
                self.retrieve_game_folder(
                    item=item
                ),
                f'{self._software.get_id().value.lower()}{Constants.XML_EXTENSION}'
            )
            if not self.__only_add_data or not FileHelper.is_file_exists(
                file_path=xml_file_path
            ):
                # Write content in a XML file
                FileHelper.write_file(
                    file_path=xml_file_path,
                    content=game_info
                )
