#!/usr/bin/python3
"""Executor to install Games"""

import os
from executor.games.abstract_games_executor import AbstractGamesExecutor
from libraries.constants.constants import Action, Constants, Media, Software
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from manager.manager_factory import ManagerFactory


class InstallGamesExecutor(AbstractGamesExecutor):
    """Executor to install Games"""

    def get_action(self) -> Action:
        """Get Action"""

        return Action.INSTALL

    def do_execution(self, item: dict):
        """Do execution for an item"""

        # Retrieve media files
        media_files: dict[Media, str] = {}
        for media in Media:
            folder_path = os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform().value,
                item[Constants.UI_TABLE_KEY_COL_ID],
                self.MEDIA_FOLDER_NAME
            )
            relative_paths = FileHelper.list_relative_paths(
                folder_path=folder_path,
                file_name=media.value,
                error_if_not_found=False
            )
            if len(relative_paths) == 0:
                continue
            media_files[media] = os.path.join(
                folder_path,
                relative_paths[0]
            )

        # Retrieve game info files
        game_info_files: dict[Software, str] = {}
        for software in Software:
            software_manager = ManagerFactory.create(
                software=software
            )
            file_path = os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform().value,
                item[Constants.UI_TABLE_KEY_COL_ID],
                f'{software_manager.get_id()}{Constants.XML_EXTENSION}'
            )
            if FileHelper.is_file_exists(
                file_path=file_path
            ):
                game_info_files[software] = file_path

        # Retrieve rom file
        rom_file = None
        folder_path = os.path.join(
            Context.get_games_path(),
            Context.get_selected_platform().value,
            item[Constants.UI_TABLE_KEY_COL_ID],
            self.ROM_FOLDER_NAME
        )
        relative_paths = FileHelper.list_relative_paths(
            folder_path=folder_path,
            file_name='*',
            error_if_not_found=False
        )
        if len(relative_paths) > 0:
            rom_file = os.path.join(
                folder_path,
                relative_paths[0]
            )

        # Install game
        self._software_manager.install_game(
            platform=Context.get_selected_platform(),
            game_item=item,
            media_files=media_files,
            game_info_files=game_info_files,
            rom_file=rom_file
        )
