#!/usr/bin/python3
"""Executor to delete Games"""

import os
from executor.games.abstract_games_executor import AbstractGamesExecutor
from libraries.constants.constants import Action, Constants
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper


class DeleteGamesExecutor(AbstractGamesExecutor):
    """Executor to delete Games"""

    def get_action(self) -> Action:
        """Get Action"""

        return Action.UNINSTALL

    def do_execution(self, item: dict):
        """Do execution for an item"""

        # Install game
        FileHelper.delete_folder(
            folder_path=os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform().value,
                item[Constants.UI_TABLE_KEY_COL_ID]
            )
        )
