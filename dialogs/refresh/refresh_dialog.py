#!/usr/bin/python3
"""Dialog to refresh the application"""

import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

from executor.games.export.export_games_executor import ExportGamesExecutor
from libraries.constants.constants import Action, Category, Component, Constants
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.ui.ui_helper import UIHelper
from libraries.xml.xml_helper import XmlHelper
from software.abstract_software import AbstractSoftware

# pylint: disable=attribute-defined-outside-init, too-many-branches
# pylint: disable=too-many-instance-attributes, too-many-statements
# pylint: disable=line-too-long, too-many-locals, too-many-lines
# pylint: disable=too-many-return-statements


class RefreshDialog:
    """Dialog to refresh the application"""

    def __init__(
        self,
        parent,
        only_ids: list[str],
        callback: any
    ):
        """Initialize dialog"""

        self.__refresh_done = False
        self.__interruption_requested = False
        self.__only_ids = only_ids
        self.__callback = callback

        # Create dialog
        self.dialog = UIHelper.create_dialog(parent)

        # Fix dialog's title
        self.dialog.title(Context.get_text(
            'refresh',
            target=Context.get_text(
                Context.get_selected_category().value
            )
        ))

        # Add a progress bar
        self.progress_bar = ttk.Progressbar(
            self.dialog,
            orient=tk.HORIZONTAL,
            length=500,
            mode='determinate'
        )
        self.progress_bar.pack(
            side=tk.TOP,
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_BIG
        )

        self.progress_label = tk.Label(
            self.dialog
        )
        self.progress_label.pack(
            side=tk.TOP
        )

        # Avoid to close the dialog
        self.dialog.protocol("WM_DELETE_WINDOW", self.__on_close)

        # Execute refresh in a thread
        execution_thread = threading.Thread(
            target=self.__refresh
        )
        execution_thread.start()

        # Fix dialog's size and position
        UIHelper.center_dialog(
            dialog=self.dialog,
            width=480,
            height=75
        )

    def __on_close(self):
        """Called when closing"""

        if self.__refresh_done or self.__interruption_requested:
            # Call back
            self.__callback()

            # Close the dialog
            UIHelper.close_dialog(self.dialog)
        else:
            # Ask if interrupt
            if messagebox.askyesno(
                Context.get_text('question'),
                Context.get_text('question_interrupt_process'),
                parent=self.dialog
            ):
                self.__interruption_requested = True

    def __is_with_only_ids(
        self
    ):
        """Specify if with only ids"""

        return self.__only_ids is not None and \
            len(self.__only_ids) > 0

    def __is_item_to_refresh(
        self,
        item_id: str
    ):
        """Specify if the id has to be refreshed"""

        if self.__is_with_only_ids():
            return item_id in self.__only_ids

        return True

    def __count_items_to_refresh(
        self,
        items: list
    ):
        """Count how many items to refresh"""

        if self.__is_with_only_ids():
            return len(self.__only_ids)

        return len(items)

    def __refresh_games_rows(self):
        """Refresh rows for GAMES"""

        # Initialize result
        result = []

        # List games with rom for selected Software
        selected_software_dict = AbstractSoftware.get_registered_software(
            software_id=Context.get_selected_software()
        ).list_games_with_rom(
            platform=Context.get_selected_platform()
        )

        # List games with rom for data
        data_dict = {}
        for game_folder in FileHelper.list_sub_directories(
            folder_path=os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform()
            )
        ):
            # Try to find the rom file
            rom_files = FileHelper.list_relative_paths(
                folder_path=os.path.join(
                    Context.get_games_path(),
                    Context.get_selected_platform(),
                    game_folder,
                    Constants.PATH_ROM
                ),
                file_name='*',
                error_if_not_found=False
            )

            if len(rom_files) == 0:
                continue

            rom_file = FileHelper.get_main_file(
                files_paths=rom_files
            )

            game_name = FileHelper.retrieve_file_basename(rom_file)
            data_dict[FileHelper.retrieve_file_name(rom_file)] = game_name

        # Set lists for source and destination depending on selected action
        source_data = {}
        destination_data = {}
        match(Context.get_selected_action()):
            case Action.EXPORT | Action.VIEW:
                source_data = selected_software_dict
                destination_data = data_dict

            case Action.INSTALL | Action.UNINSTALL | Action.DELETE | Action.EDIT | Action.COPY:
                source_data = data_dict
                destination_data = selected_software_dict

        # Initialize progress bar
        item_current_counter = 0
        item_total_counter = self.__count_items_to_refresh(
            items=source_data
        )
        self.progress_bar.config(
            maximum=item_total_counter
        )

        # Add rows
        for rom, name in source_data.items():
            item_id = FileHelper.retrieve_file_basename(
                rom
            )

            # Ignore item to refresh if requested
            if not self.__is_item_to_refresh(item_id):
                continue

            # Interrupt process if requested
            if self.__interruption_requested:
                self.__on_close()
                return result

            # Increment progress bar
            item_current_counter += 1
            self.progress_bar['value'] = item_current_counter
            self.progress_label.config(
                text=Context.get_text(
                    'refresh_in_progress',
                    item_name=name,
                    item_current_counter=item_current_counter,
                    item_total_counter=item_total_counter
                )
            )

            # Waiting 0.1 seconde to see the dialog if the process is quick
            time.sleep(0.1)

            # Build row
            row = {}
            row[Constants.UI_TABLE_KEY_COL_SELECTION] = False
            row[Constants.UI_TABLE_KEY_COL_ID] = item_id
            row[Constants.UI_TABLE_KEY_COL_NAME] = name
            row[Constants.UI_TABLE_KEY_COL_ROM] = rom

            # If source is data, try to extract the name from software if possible
            if source_data == data_dict:
                for software in Context.list_available_softwares():
                    software = AbstractSoftware.get_registered_software(
                        software_id=software
                    )
                    software_games = software.list_games_with_rom(
                        platform=Context.get_selected_platform()
                    )
                    if rom not in software_games:
                        continue
                    if len(software_games[rom]) == 0:
                        continue
                    row[Constants.UI_TABLE_KEY_COL_NAME] = software_games[rom]
                    break

            # Check if unique
            row[Constants.UI_TABLE_KEY_COL_UNIQUE] = list(
                source_data.values()
            ).count(row[Constants.UI_TABLE_KEY_COL_NAME]) <= 1

            # Retrieve color depending on selected action
            match(Context.get_selected_action()):
                case Action.EXPORT:
                    rom_path = ExportGamesExecutor.retrieve_rom_path(
                        item=row
                    )
                    if rom_path not in destination_data:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_RED
                    elif not row[Constants.UI_TABLE_KEY_COL_UNIQUE]:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_ORANGE
                    else:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_GREEN

                case Action.INSTALL | Action.UNINSTALL:
                    if row[Constants.UI_TABLE_KEY_COL_ROM] not in destination_data:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_RED
                    elif not row[Constants.UI_TABLE_KEY_COL_UNIQUE]:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_ORANGE
                    else:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_GREEN

                case Action.DELETE | Action.EDIT | Action.VIEW | Action.COPY:
                    if not row[Constants.UI_TABLE_KEY_COL_UNIQUE]:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_ORANGE
                    else:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_GREEN

            # Append row
            result.append(row)

        return result

    def __refresh_platforms_rows(self):
        """Refresh rows for PLATFORMS"""

        # Initialize result
        result = []

        # Initialize list platforms depending on selected action
        if Context.get_selected_action() == Action.DELETE:
            list_platforms = Context.list_available_platforms()
        else:
            list_platforms = AbstractSoftware.get_registered_software(
                software_id=Context.get_selected_software()
            ).list_platforms()

        # List platforms with games counter for selected Software
        selected_software_dict = {}
        for platform in list_platforms:
            # Retrieve platform's games
            platform_games = AbstractSoftware.get_registered_software(
                software_id=Context.get_selected_software()
            ).list_games_with_rom(
                platform=platform
            )

            selected_software_dict[platform] = len(
                platform_games
            )

        # List platforms with games counter for data
        data_dict = {}
        for platform_folder in FileHelper.list_sub_directories(
            folder_path=os.path.join(
                Context.get_games_path()
            )
        ):
            # If platform is not a platform for the selected software
            if platform_folder not in list_platforms:
                continue

            # Count games for platform
            games_counter = len(
                FileHelper.list_sub_directories(
                    folder_path=os.path.join(
                        Context.get_games_path(),
                        platform_folder
                    )
                )
            )

            data_dict[platform_folder] = games_counter

        # Set lists for source and destination depending on selected action
        source_data = {}
        destination_data = {}
        match(Context.get_selected_action()):
            case Action.EXPORT:
                source_data = selected_software_dict
                destination_data = data_dict

            case Action.INSTALL | Action.UNINSTALL | Action.DELETE | Action.COPY:
                source_data = data_dict
                destination_data = selected_software_dict

        # Initialize progress bar
        item_current_counter = 0
        item_total_counter = self.__count_items_to_refresh(
            items=source_data
        )
        self.progress_bar.config(
            maximum=item_total_counter
        )

        # Add rows
        for platform, games_counter in source_data.items():
            item_id = platform

            # Ignore item to refresh if requested
            if not self.__is_item_to_refresh(item_id):
                continue

            # Interrupt process if requested
            if self.__interruption_requested:
                self.__on_close()
                return result

            # Increment progress bar
            item_current_counter += 1
            self.progress_bar['value'] = item_current_counter
            self.progress_label.config(
                text=Context.get_text(
                    'refresh_in_progress',
                    item_name=platform,
                    item_current_counter=item_current_counter,
                    item_total_counter=item_total_counter
                )
            )

            # Waiting 0.1 seconde to see the dialog if the process is quick
            time.sleep(0.1)

            # If source is data and action != DELETE, ignore platform not managed by the software
            if source_data == data_dict and \
                    Context.get_selected_action() not in [Action.DELETE] and \
                    platform not in destination_data:
                continue

            # Build row
            row = {}
            row[Constants.UI_TABLE_KEY_COL_SELECTION] = False
            row[Constants.UI_TABLE_KEY_COL_ID] = item_id
            row[Constants.UI_TABLE_KEY_COL_NAME] = platform
            row[Constants.UI_TABLE_KEY_COL_GAMES] = str(games_counter)

            # Retrieve color depending on selected action
            match(Context.get_selected_action()):
                case Action.EXPORT | Action.INSTALL | Action.UNINSTALL:
                    platform_name = row[Constants.UI_TABLE_KEY_COL_NAME]
                    if platform_name not in destination_data:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_RED
                    elif destination_data[platform_name] == 0:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_RED
                    elif destination_data[platform_name] < games_counter:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_ORANGE
                    else:
                        row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_GREEN

                case Action.DELETE | Action.COPY:
                    row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_GREEN

            # Append row
            result.append(row)

        return result

    def __refresh_configs_rows(self):
        """Refresh rows for CONFIGS"""

        # Initialize result
        result = []

        # Add rows
        for config in FileHelper.list_sub_directories(
            folder_path=Context.get_configs_path()
        ):
            item_id = config

            # Ignore item to refresh if requested
            if not self.__is_item_to_refresh(item_id):
                continue

            # Waiting 0.1 seconde to see the dialog if the process is quick
            time.sleep(0.1)

            # Build row
            row = {}
            row[Constants.UI_TABLE_KEY_COL_SELECTION] = False
            row[Constants.UI_TABLE_KEY_COL_ID] = item_id
            row[Constants.UI_TABLE_KEY_COL_NAME] = config
            row[Component.FILES.value] = FileHelper.is_folder_exists(
                folder_path=os.path.join(
                    Context.get_configs_path(),
                    config,
                    Component.FILES.name.lower()
                )
            )
            row[Component.REGISTRY.value] = FileHelper.is_folder_exists(
                folder_path=os.path.join(
                    Context.get_configs_path(),
                    config,
                    Component.REGISTRY.name.lower()
                )
            )

            # Retrieve color
            row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_GREEN

            # Append row
            result.append(row)

        return result

    def __refresh(self):
        """Refresh"""

        # Refresh rows depending on selected category
        rows = []
        match(Context.get_selected_category()):
            case Category.GAMES:
                rows = self.__refresh_games_rows()

            case Category.PLATFORMS:
                rows = self.__refresh_platforms_rows()

            case Category.CONFIGS:
                rows = self.__refresh_configs_rows()

        # If with only ids, add rows not refreshed from CSV rows
        if self.__is_with_only_ids():
            for row in XmlHelper.load_xml(
                xml_file_path=Context.get_selected_rows_cache_path()
            ):
                if self.__is_item_to_refresh(
                    item_id=row[Constants.UI_TABLE_KEY_COL_ID]
                ):
                    continue

                rows.append(row)

        # Sort rows depending on UI_TABLE_KEY_COLOR (desc) and Constants.UI_TABLE_KEY_COL_NAME (asc)
        rows = sorted(
            rows,
            key=lambda x: (-ord(
                x[Constants.UI_TABLE_KEY_COLOR][0]),
                x[Constants.UI_TABLE_KEY_COL_NAME]
            )
        )

        # Finish progression
        if len(rows) > 0:
            self.progress_bar['value'] = len(rows)
        else:
            self.progress_bar.config(maximum=1)
            self.progress_bar['value'] = 1
        self.progress_label.config(
            text=Context.get_text('refresh_finished')
        )

        # Write data in a cache file
        XmlHelper.save_xml(
            xml_file_path=Context.get_selected_rows_cache_path(),
            root_tag=Constants.CACHE_TAG_ROOT,
            obj=rows,
            force=True
        )

        # Specify that refresh is done
        self.__refresh_done = True

        # Close automatically
        self.__on_close()
