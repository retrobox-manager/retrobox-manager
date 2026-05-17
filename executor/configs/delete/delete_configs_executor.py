#!/usr/bin/python3
"""Executor to delete Configs"""

import os
from executor.configs.abstract_configs_executor import AbstractConfigsExecutor
from libraries.constants.constants import Action, Component, Constants
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper


class DeleteConfigsExecutor(AbstractConfigsExecutor):
    """Executor to delete Configs"""

    def get_action(self) -> Action:
        """Get Action"""

        return Action.DELETE

    def do_execution(self, item: dict):
        """Do execution for an item"""

        # Delete files if requested
        if Component.FILES in Context.get_selected_components():
            FileHelper.delete_folder(
                folder_path=os.path.join(
                    Context.get_configs_path(),
                    item[Constants.UI_TABLE_KEY_COL_ID],
                    Component.FILES.name.lower()
                )
            )

        # Delete registry if requested
        if Component.REGISTRY in Context.get_selected_components():
            FileHelper.delete_folder(
                folder_path=os.path.join(
                    Context.get_configs_path(),
                    item[Constants.UI_TABLE_KEY_COL_ID],
                    Component.REGISTRY.name.lower()
                )
            )

        # Delete config if empty
        files, folders = FileHelper.list_files_and_folders(
            folder_path=os.path.join(
                Context.get_configs_path(),
                item[Constants.UI_TABLE_KEY_COL_ID]
            )
        )
        if len(files) == 0 and len(folders) == 0:
            FileHelper.delete_folder(
                folder_path=os.path.join(
                    Context.get_configs_path(),
                    item[Constants.UI_TABLE_KEY_COL_ID]
                )
            )
