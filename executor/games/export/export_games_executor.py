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
            game_item=item
        ).items():
            # Retrieve destination's file
            destination_file_path = os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform().value,
                item[Constants.UI_TABLE_KEY_COL_ID],
                self.MEDIA_FOLDER_NAME,
                f'{media.value}{FileHelper.retrieve_file_extension(
                    file_path=file_path
                )}'
            )

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
        rom_file = self._software_manager.retrieve_rom_file(
            platform=Context.get_selected_platform(),
            game_item=item
        )
        if rom_file is not None or FileHelper.is_file_exists(
            file_path=rom_file
        ):
            # Retrieve destination's file
            destination_file_path = os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform().value,
                item[Constants.UI_TABLE_KEY_COL_ID],
                self.ROM_FOLDER_NAME,
                FileHelper.retrieve_file_name(rom_file)
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

        # Retrieve game's info
        game_info = self._software_manager.retrieve_game_info(
            platform=Context.get_selected_platform(),
            game_item=item
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
