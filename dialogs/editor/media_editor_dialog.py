#!/usr/bin/python3
"""Dialog to edit media"""

import tkinter as tk
import os
from tkinter import ttk

from libraries.constants.constants import Action, Category, Constants, Media, SoftwareId
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.ui.ui_helper import UIHelper
from libraries.ui.ui_media_grid import UIMediaGrid
from libraries.ui.ui_table import UITable
from software.abstract_software import AbstractSoftware

# pylint: disable=attribute-defined-outside-init, too-many-locals
# pylint: disable=too-many-instance-attributes, too-many-statements
# pylint: disable=too-many-branches


class MediaEditorDialog:
    """Dialog to edit media"""

    def __init__(
        self,
        parent,
        callback: any = None
    ):
        """Initialize dialog"""

        self.__callback: any = callback
        self.__table: UITable = None
        self.__current_item: dict = None

        # Create dialog
        self.__dialog = UIHelper.create_dialog(parent)

        # Fix dialog's title
        self.__dialog.title(Context.get_text('edit_media'))

        # Force bg to avoid black panel when loading
        self.__dialog.configure(bg="SystemButtonFace")

        # Create top frame
        self.__top_frame = tk.Frame(
            self.__dialog
        )
        self.__top_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True
        )

        # Create bottom frame
        self.__bottom_frame = tk.Frame(
            self.__dialog
        )
        self.__bottom_frame.pack(
            side=tk.BOTTOM,
            fill=tk.BOTH,
            pady=Constants.UI_PAD_SMALL
        )

        # Create components
        self.__create_category_components()
        self.__create_media_components()
        self.__create_close_components()

        # Bind closing event
        self.__dialog.protocol("WM_DELETE_WINDOW", self.__on_close)

        # Select the software to show
        if Context.get_selected_action() == Action.VIEW:
            self.__current_software = Context.get_selected_software()
        else:
            self.__current_software = Context.list_available_softwares()[0]
        self.__software_combo.current(
            list(SoftwareId).index(self.__current_software)
        )

        # Select the first row
        self.__table.set_selected_rows([0])

        # Fix dialog's size and position
        UIHelper.center_dialog(
            dialog=self.__dialog,
            width=1800,
            height=1370
        )

    def __create_category_components(self):
        """Create category components"""

        # Create category frames
        category_label_frame = tk.LabelFrame(
            self.__top_frame,
            text=Context.get_text(Context.get_selected_category().value)
        )
        category_label_frame.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_BIG
        )
        category_actions_frame = tk.Frame(category_label_frame)
        category_actions_frame.pack(
            side=tk.TOP,
            fill=tk.Y
        )
        category_frame = tk.Frame(category_label_frame)
        category_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            pady=Constants.UI_PAD_SMALL
        )

        # Build rows
        selected_rows = []
        match(Context.get_selected_category()):
            case Category.GAMES:
                selected_rows = Context.get_selected_rows()

        rows = []
        for selected_row in selected_rows:
            row = {
                Constants.UI_TABLE_KEY_COL_SELECTION: False,
                Constants.UI_TABLE_KEY_COL_ID: selected_row[Constants.UI_TABLE_KEY_COL_ID],
                Constants.UI_TABLE_KEY_COL_NAME: selected_row[Constants.UI_TABLE_KEY_COL_NAME],
                Constants.UI_TABLE_KEY_COL_ROM: selected_row[Constants.UI_TABLE_KEY_COL_ROM],
                Constants.UI_TABLE_KEY_COL_UNIQUE: selected_row[Constants.UI_TABLE_KEY_COL_UNIQUE],
                Constants.UI_TABLE_KEY_COLOR: selected_row[Constants.UI_TABLE_KEY_COLOR]
            }

            rows.append(row)

        # Create table
        self.__table = UITable(
            parent=category_frame,
            on_selected_rows_change=self.__on_selected_rows_changed,
            rows=rows,
            multiple_selection=False
        )

    def __create_media_components(self):
        """Create media components"""

        # Create media frames
        media_label_frame = tk.LabelFrame(
            self.__top_frame,
            text=Context.get_text('media_title')
        )
        media_label_frame.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_BIG
        )
        media_actions_frame = tk.Frame(media_label_frame)
        media_actions_frame.pack(
            side=tk.TOP,
            fill=tk.Y
        )

        # Create Combobox for software
        software_label = tk.Label(
            media_actions_frame,
            text=Context.get_text('software')
        )
        software_label.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

        available_softwares = []
        for software in SoftwareId:
            if software in Context.list_available_softwares():
                available_softwares.append(software.value)
        available_softwares.sort()
        self.__software_combo = ttk.Combobox(
            media_actions_frame,
            values=available_softwares
        )
        self.__software_combo.config(state="readonly")
        self.__software_combo.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.__software_combo.bind(
            "<<ComboboxSelected>>", self.__on_software_changed)

        # Add description frame
        description_frame = tk.Frame(media_label_frame)
        description_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )

        # Label for description
        self.__description_label = tk.Label(
            description_frame,
            anchor=tk.N
        )
        self.__description_label.pack(
            side=tk.LEFT,
            fill=tk.BOTH
        )

        # Create component for the description
        self.__description_text = tk.Text(
            description_frame,
            wrap=tk.WORD,
            height=3,
            width=40
        )
        self.__description_text.pack(
            fill=tk.BOTH,
            expand=True
        )

        # Disable modification for the description
        self.__description_text.config(state='disabled')

        # Create media grid
        media_frame = tk.Frame(media_label_frame)
        media_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH
        )
        self.__media_grid = UIMediaGrid(
            parent=media_frame,
            rows=5,
            columns=5,
            cell_width=200,
            cell_height=200,
            read_only=Context.get_selected_action() == Action.VIEW
        )
        self.__media_grid.pack(
            fill=tk.BOTH
        )

    def __create_close_components(self):
        """Create close components"""

        # Create button to close
        button_close = tk.Button(
            self.__bottom_frame,
            text=Context.get_text('close'),
            command=self.__on_close
        )
        button_close.pack(
            side=tk.TOP
        )

    def __on_close(self):
        """Called when closing"""

        # Stop all media components
        for media_component in self.__media_grid.list_media():
            media_component.stop_media()

        # Refresh data
        if self.__callback is not None:
            self.__callback(
                only_ids=Context.get_selected_rows()
            )

        # Close the dialog
        UIHelper.close_dialog(self.__dialog)

    def __on_selected_rows_changed(self):
        """Called when selected rows changed"""

        # Retrieve selected rows
        selected_rows = self.__table.get_selected_rows()

        # Do nothing if no selected row
        if len(selected_rows) != 1:
            return

        # Retrieve selected item
        self.__current_item = selected_rows[0]

        # Update all media components
        self.__update_all_components()

    def __on_software_changed(self, event):
        """Called when a software changed"""

        # Change current software
        self.__current_software = None
        for software in SoftwareId:
            if software.value == event.widget.get():
                self.__current_software = software

        self.__table.focus()

        # Update all media components
        self.__update_all_components()

    def __update_all_components(self):
        """Update all components"""

        # Do nothing if missing current software
        if self.__current_software is None:
            return

        # Retrieve game info software id depending on the selected action
        if Context.get_selected_action() == Action.VIEW:
            game_info_software_id = self.__current_software
        else:
            game_info_software_id = AbstractSoftware.get_registered_software(
                software_id=self.__current_software
            ).retrieve_retrobox_manager_game_info_software_id(
                platform=Context.get_selected_platform(),
                game_item=self.__current_item
            )

        # Create the game info software
        game_info_software = AbstractSoftware.get_registered_software(
            software_id=game_info_software_id
        )

        # Update label for description
        self.__description_label.configure(
            text=Context.get_text(
                'media_description_source',
                source=game_info_software_id.value
            )
        )

        # Set description from current software
        current_game_description = game_info_software.retrieve_game_description(
            game_info_path=game_info_software.retrieve_software_game_info_path(
                platform=Context.get_selected_platform(),
                game_item=self.__current_item
            ),
            platform=Context.get_selected_platform(),
            game_item=self.__current_item
        )

        # Update description's text
        self.__description_text.config(state='normal')
        self.__description_text.delete("1.0", tk.END)
        self.__description_text.insert(
            tk.END,
            current_game_description
        )
        self.__description_text.config(state='disabled')

        # Retrieve the media path depending on the selected action
        media_files = {}
        match(Context.get_selected_action()):
            case Action.EDIT:
                media_folder = os.path.join(
                    Context.get_games_path(),
                    Context.get_selected_platform(),
                    self.__current_item[Constants.UI_TABLE_KEY_COL_ID],
                    Constants.PATH_MEDIA
                )

                # Retrieve relative paths for media
                for media in Media:
                    relative_paths = FileHelper.list_relative_paths(
                        folder_path=media_folder,
                        file_name=media.name.lower(),
                        error_if_not_found=False
                    )
                    if len(relative_paths) == 1:
                        media_files[media] = os.path.join(
                            media_folder,
                            relative_paths[0]
                        )

            case Action.VIEW:
                media_files = AbstractSoftware.get_registered_software(
                    software_id=self.__current_software
                ).retrieve_media_files(
                    platform=Context.get_selected_platform(),
                    game_item=self.__current_item
                )

        # Retrieve the default media's folder
        default_media_folder = os.path.join(
            Context.get_games_path(),
            Context.get_selected_platform(),
            self.__current_item[Constants.UI_TABLE_KEY_COL_ID],
            Constants.PATH_MEDIA
        )

        # Update all media
        for row in range(self.__media_grid.rows):
            for column in range(self.__media_grid.columns):
                # Retrieve the media at the position
                media = AbstractSoftware.get_registered_software(
                    software_id=self.__current_software
                ).get_context().media_positions.get(
                    (row, column),
                    None
                )

                # Update media depending on media position
                media_title = None
                media_folder = default_media_folder
                media_file = None
                if media is not None:

                    # Retrieve media title
                    media_title = Context.get_text(media.value)

                    # Retrieve media file
                    media_file = media_files.get(
                        media, None
                    )

                    # Retrieve media folder
                    if media_file is not None:
                        media_folder = FileHelper.retrieve_file_parent(
                            media_file
                        )

                # Retrieve media component from the grid
                media_component = self.__media_grid.get_media(
                    row=row,
                    column=column
                )

                # Update the media component
                media_component.update_media(
                    media=media,
                    media_title=media_title,
                    media_folder=media_folder,
                    media_file=media_file
                )
