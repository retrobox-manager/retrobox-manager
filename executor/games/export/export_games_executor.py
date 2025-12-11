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

        # Copy files for media
        for media, file_path in self._software_manager.retrieve_media_files(
            platform=Context.get_selected_platform(),
            game=item[Constants.UI_TABLE_KEY_COL_NAME]
        ).items():
            # Retrieve destination's folder
            destination_folder = os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform().value,
                item[Constants.UI_TABLE_KEY_COL_ID],
                self._MEDIA_FOLDER_NAME,
                media.value
            )

            # Delete destination's folder
            FileHelper.delete_folder(
                folder_path=destination_folder
            )

            # Copy file in destination's folder
            FileHelper.copy_file(
                source_file_path=file_path,
                destination_file_path=os.path.join(
                    destination_folder,
                    os.path.basename(file_path)
                )
            )

        # Copy rom
        rom_file = self._software_manager.retrieve_rom_file(
            platform=Context.get_selected_platform(),
            game=item[Constants.UI_TABLE_KEY_COL_NAME]
        )
        if rom_file is not None or FileHelper.is_file_exists(
            file_path=rom_file
        ):
            # Retrieve destination's folder
            destination_folder = os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform().value,
                item[Constants.UI_TABLE_KEY_COL_ID],
                self._ROM_FOLDER_NAME,
            )

            # Delete destination's folder
            FileHelper.delete_folder(
                folder_path=destination_folder
            )

            # Copy file in destination's folder
            FileHelper.copy_file(
                source_file_path=rom_file,
                destination_file_path=os.path.join(
                    destination_folder,
                    os.path.basename(rom_file)
                )
            )

        # Retrieve game's info
        game_info = self._software_manager.retrieve_game_info(
            platform=Context.get_selected_platform(),
            game=item[Constants.UI_TABLE_KEY_COL_NAME]
        )

        # Write content in a XML file
        FileHelper.write_file(
            file_path=os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform().value,
                item[Constants.UI_TABLE_KEY_COL_ID],
                f'{self._software_manager.get_id()}{Constants.XML_EXTENSION}'
            ),
            content=game_info
        )
