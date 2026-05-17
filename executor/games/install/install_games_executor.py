#!/usr/bin/python3
"""Executor to install Games"""

import os
from executor.games.abstract_games_executor import AbstractGamesExecutor
from libraries.constants.constants import Action, Constants, Media
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper


class InstallGamesExecutor(AbstractGamesExecutor):
    """Executor to install Games"""

    def get_action(self) -> Action:
        """Get Action"""

        return Action.INSTALL

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

        # Retrieve media files
        media_files: dict[Media, str] = {}
        for media in Media:
            folder_path = os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform(),
                item[Constants.UI_TABLE_KEY_COL_ID],
                Constants.PATH_MEDIA
            )
            relative_path = FileHelper.get_main_file(
                files_paths=FileHelper.list_relative_paths(
                    folder_path=folder_path,
                    file_name=media.name.lower(),
                    error_if_not_found=False
                )
            )

            if relative_path is None:
                continue

            media_files[media] = os.path.join(
                folder_path,
                relative_path
            )

        # Retrieve rom file
        rom_file = None
        folder_path = os.path.join(
            Context.get_games_path(),
            Context.get_selected_platform(),
            item[Constants.UI_TABLE_KEY_COL_ID],
            Constants.PATH_ROM
        )
        relative_path = FileHelper.get_main_file(
            files_paths=FileHelper.list_relative_paths(
                folder_path=folder_path,
                file_name='*',
                error_if_not_found=False
            )
        )

        if relative_path is not None:
            rom_file = os.path.join(
                folder_path,
                relative_path
            )

        # Install game
        self._software.install_game(
            platform=Context.get_selected_platform(),
            game_item=item,
            media_files=media_files,
            rom_file=rom_file
        )
