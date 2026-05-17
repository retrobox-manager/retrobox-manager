#!/usr/bin/python3
"""Executor to uninstall Games"""

import os
from executor.games.abstract_games_executor import AbstractGamesExecutor
from libraries.constants.constants import Action, Constants
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper


class UninstallGamesExecutor(AbstractGamesExecutor):
    """Executor to uninstall Games"""

    def get_action(self) -> Action:
        """Get Action"""

        return Action.UNINSTALL

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
                error_if_not_found=False
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

        # Install game
        self._software.uninstall_game(
            platform=Context.get_selected_platform(),
            game_item=item
        )
