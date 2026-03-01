#!/usr/bin/python3
"""Executor Factory"""

from executor.abstract_executor import AbstractExecutor
from executor.configs.delete.delete_configs_executor import DeleteConfigsExecutor
from executor.configs.install.install_configs_executor import InstallConfigsExecutor
from executor.configs.uninstall.uninstall_configs_executor import UninstallConfigsExecutor
from executor.games.copy.copy_games_executor import CopyGamesExecutor
from executor.games.delete.delete_games_executor import DeleteGamesExecutor
from executor.games.export.export_games_executor import ExportGamesExecutor
from executor.games.install.install_games_executor import InstallGamesExecutor
from executor.games.uninstall.uninstall_games_executor import UninstallGamesExecutor
from libraries.constants.constants import Action, Category
from libraries.context.context import Context

# pylint: disable=too-many-return-statements


class ExecutorFactory:
    """Executor Factory"""

    @staticmethod
    def create() -> AbstractExecutor:
        """Create Executor"""

        if Context.get_selected_category() == Category.GAMES:
            match(Context.get_selected_action()):
                case Action.EXPORT:
                    return ExportGamesExecutor()
                case Action.INSTALL:
                    return InstallGamesExecutor()
                case Action.UNINSTALL:
                    return UninstallGamesExecutor()
                case Action.DELETE:
                    return DeleteGamesExecutor()
                case Action.COPY:
                    return CopyGamesExecutor()
        elif Context.get_selected_category() == Category.PLATFORMS:
            match(Context.get_selected_action()):
                case Action.EXPORT:
                    return ExportGamesExecutor(
                        sub_items_enabled=True
                    )
                case Action.INSTALL:
                    return InstallGamesExecutor(
                        sub_items_enabled=True
                    )
                case Action.UNINSTALL:
                    return UninstallGamesExecutor(
                        sub_items_enabled=True
                    )
                case Action.DELETE:
                    return DeleteGamesExecutor(
                        sub_items_enabled=True
                    )
                case Action.COPY:
                    return CopyGamesExecutor(
                        sub_items_enabled=True
                    )
        elif Context.get_selected_category() == Category.CONFIGS:
            match(Context.get_selected_action()):
                case Action.INSTALL:
                    return InstallConfigsExecutor()
                case Action.UNINSTALL:
                    return UninstallConfigsExecutor()
                case Action.DELETE:
                    return DeleteConfigsExecutor()

        return None
