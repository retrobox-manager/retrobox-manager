#!/usr/bin/python3
"""Executor to export Games"""

import os
from executor.games.abstract_games_executor import AbstractGamesExecutor
from libraries.constants.constants import Action, Constants
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper


class ExportGamesExecutor(AbstractGamesExecutor):
    """Executor to export Games"""

    def get_action(self) -> Action:
        """Get Action"""

        return Action.EXPORT

    def do_execution(self, item: dict):
        """Do execution for an item"""

        # Retrieve the media files for the game
        game_files = self._front_end.retrieve_game_files(
            platform=Context.get_selected_platform(),
            game=item[Constants.UI_TABLE_KEY_COL_NAME]
        )

        # Copy files for rom and media
        for file_id, file_path in game_files.items():
            folder = ''
            if file_id == self._front_end.get_rom_key():
                folder = self._ROM_FOLDER_NAME
            else:
                folder = os.path.join(
                    self._MEDIA_FOLDER_NAME,
                    file_id
                )
            FileHelper.copy_file(
                source_file_path=file_path,
                destination_file_path=os.path.join(
                    Context.get_games_path(),
                    self._platform_data[self._TAG_NAME],
                    item[Constants.UI_TABLE_KEY_COL_ID],
                    folder,
                    os.path.basename(file_path)
                )
            )

        # Retrieve game's info
        game_info = self._front_end.retrieve_game_info(
            platform=Context.get_selected_platform(),
            game=item[Constants.UI_TABLE_KEY_COL_NAME]
        )

        # Write content in a XML file
        FileHelper.write_file(
            file_path=os.path.join(
                Context.get_games_path(),
                self._platform_data[self._TAG_NAME],
                item[Constants.UI_TABLE_KEY_COL_ID],
                f'{self._front_end.get_id()}{Constants.XML_EXTENSION}'
            ),
            content=game_info
        )
