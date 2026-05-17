#!/usr/bin/python3
"""Executor to copy Games"""

import os
from datetime import datetime
from executor.games.abstract_games_executor import AbstractGamesExecutor
from libraries.constants.constants import Action, Component, Constants
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper


class CopyGamesExecutor(AbstractGamesExecutor):
    """Executor to copy Games"""

    def __init__(
        self,
        sub_items_enabled: bool = False
    ):
        """Initialize executor"""

        super().__init__(
            sub_items_enabled=sub_items_enabled
        )

        # Retrieve current timestamp
        self.__curent_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def get_action(self) -> Action:
        """Get Action"""

        return Action.COPY

    def list_sub_items(self, item: dict) -> list[dict]:
        """List sub items for the current item"""

        # Initialize result
        result: list[dict] = []

        # Select the platform
        Context.set_selected_platform(
            platform=item[Constants.UI_TABLE_KEY_COL_ID]
        )

        # List games with rom from the selected sofware
        games_with_rom = self._software.list_games_with_rom(
            platform=Context.get_selected_platform()
        )

        # List games with rom for data and selected Platform
        _, folders = FileHelper.list_files_and_folders(
            folder_path=os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform()
            )
        )
        for game_folder in folders:
            # Try to find the rom file
            rom_files = FileHelper.list_relative_paths(
                folder_path=os.path.join(
                    Context.get_games_path(),
                    Context.get_selected_platform(),
                    game_folder,
                    Constants.PATH_ROM
                ),
                file_name='*',
                error_if_not_found=False,
            )

            if len(rom_files) == 0:
                continue

            rom_file = FileHelper.get_main_file(
                files_paths=rom_files
            )

            # Retrieve the game's name
            game_name = games_with_rom.get(
                rom_file, FileHelper.retrieve_file_basename(rom_file))

            # Build sub item
            sub_item = {}
            sub_item[Constants.UI_TABLE_KEY_COL_ID] = FileHelper.retrieve_file_basename(
                rom_file
            )
            sub_item[Constants.UI_TABLE_KEY_COL_NAME] = game_name
            sub_item[Constants.UI_TABLE_KEY_COL_ROM] = rom_file

            # Add sub item
            result.append(sub_item)

        return result

    def do_execution(self, item: dict):
        """Do execution for an item"""

        # Retrieve game folder
        game_folder = os.path.join(
            Context.get_games_path(),
            Context.get_selected_platform(),
            item[Constants.UI_TABLE_KEY_COL_ID]
        )

        # Retrieve destination folder
        copy_folder_name = 'copy'
        copy_folder_name += '_'
        copy_folder_name += Context.get_selected_software().value.replace(' ', '_').lower()
        copy_folder_name += '_'
        copy_folder_name += Context.get_selected_platform().replace(' ', '_').lower()
        copy_folder_name += '_'
        copy_folder_name += self.__curent_timestamp
        destination_folder_path = os.path.join(
            Context.get_selected_folder_path(),
            copy_folder_name,
            item[Constants.UI_TABLE_KEY_COL_ID]
        )

        # Copy game if all components requested
        if Component.ROM in Context.get_selected_components() and \
                Component.MEDIA in Context.get_selected_components():
            FileHelper.copy_folder(
                source_folder_path=game_folder,
                destination_folder_path=destination_folder_path
            )
            return

        # Copy rom if requested
        if Component.ROM in Context.get_selected_components():
            FileHelper.copy_folder(
                source_folder_path=os.path.join(
                    game_folder,
                    Constants.PATH_ROM
                ),
                destination_folder_path=destination_folder_path
            )

        # Copy media if requested
        if Component.MEDIA in Context.get_selected_components():
            FileHelper.copy_folder(
                source_folder_path=os.path.join(
                    game_folder,
                    Constants.PATH_MEDIA
                ),
                destination_folder_path=destination_folder_path
            )
