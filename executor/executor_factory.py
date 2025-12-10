#!/usr/bin/python3
"""Executor Factory"""

from executor.abstract_executor import AbstractExecutor
from executor.games.export.export_games_executor import ExportGamesExecutor
from libraries.constants.constants import Action, Category
from libraries.context.context import Context


class ExecutorFactory:
    """Executor Factory"""

    @staticmethod
    def create() -> AbstractExecutor:
        """Create Executor"""

        if Context.get_selected_category() == Category.GAMES:
            match(Context.get_selected_action()):
                case Action.EXPORT:
                    return ExportGamesExecutor()

        return None
