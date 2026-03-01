#!/usr/bin/python3
"""Executor to uninstall Configs"""

import os
from executor.configs.abstract_configs_executor import AbstractConfigsExecutor
from libraries.constants.constants import Action, Component, Constants
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.winreg.winreg_helper import WinRegHelper


class UninstallConfigsExecutor(AbstractConfigsExecutor):
    """Executor to uninstall Configs"""

    def get_action(self) -> Action:
        """Get Action"""

        return Action.UNINSTALL

    def do_execution(self, item: dict):
        """Do execution for an item"""

        # Uninstall FILES
        if Component.FILES in Context.get_selected_components():
            config_path = os.path.join(
                Context.get_configs_path(),
                item[Constants.UI_TABLE_KEY_COL_ID],
                Component.FILES.name.lower()
            )
            for relative_path in FileHelper.list_relative_paths(
                folder_path=config_path,
                file_name='*',
                error_if_not_found=False
            ):
                FileHelper.delete_file(
                    file_path=os.path.join(
                        self._software.get_drive(),
                        relative_path
                    )
                )

        # Uninstall REGISTRY
        if Component.REGISTRY in Context.get_selected_components():
            config_path = os.path.join(
                Context.get_configs_path(),
                item[Constants.UI_TABLE_KEY_COL_ID],
                Component.REGISTRY.name.lower()
            )
            for relative_path in FileHelper.list_relative_paths(
                folder_path=config_path,
                file_name='*',
                error_if_not_found=False
            ):
                for key in WinRegHelper.extract_regedit_keys(
                    file_path=os.path.join(
                        config_path,
                        relative_path
                    )
                ):
                    if not key.startswith(Constants.REGEDIT_ROOT_KEY_NAME):
                        continue

                    WinRegHelper.delete_user_key(
                        key=key[len(Constants.REGEDIT_ROOT_KEY_NAME) + 1:]
                    )
