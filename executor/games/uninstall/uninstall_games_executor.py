#!/usr/bin/python3
"""Executor to uninstall Games"""

from executor.games.abstract_games_executor import AbstractGamesExecutor
from libraries.constants.constants import Action
from libraries.context.context import Context


class UninstallGamesExecutor(AbstractGamesExecutor):
    """Executor to uninstall Games"""

    def get_action(self) -> Action:
        """Get Action"""

        return Action.UNINSTALL

    def do_execution(self, item: dict):
        """Do execution for an item"""

        # Install game
        self._software_manager.uninstall_game(
            platform=Context.get_selected_platform(),
            game_item=item
        )
