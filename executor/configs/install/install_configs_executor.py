#!/usr/bin/python3
"""Executor to install Configs"""

import os
from executor.configs.abstract_configs_executor import AbstractConfigsExecutor
from libraries.constants.constants import Action, Component, Constants
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.winreg.winreg_helper import WinRegHelper


class InstallConfigsExecutor(AbstractConfigsExecutor):
    """Executor to install Configs"""

    def get_action(self) -> Action:
        """Get Action"""

        return Action.INSTALL

    def do_execution(self, item: dict):
        """Do execution for an item"""

        # Install FILES
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
                FileHelper.copy_file(
                    source_file_path=os.path.join(
                        config_path,
                        relative_path
                    ),
                    destination_file_path=os.path.join(
                        self._software.get_drive(),
                        relative_path
                    )
                )

        # Install REGISTRY
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
                WinRegHelper.import_user_key(
                    extracted_file_path=os.path.join(
                        config_path,
                        relative_path
                    )
                )
