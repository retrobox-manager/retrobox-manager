#!/usr/bin/python3
"""Dialog to setup the application"""

import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

from dialogs.selection.selection_dialog import SelectionDialog
from libraries.constants.constants import Constants, Media, SoftwareId
from libraries.context.context import Context
from libraries.ui.ui_helper import UIHelper
from libraries.ui.ui_button_grid import UIButtonGrid
from libraries.ui.ui_table import UITable
from libraries.xml.xml_helper import XmlHelper
from software.abstract_software import AbstractSoftware

# pylint: disable=attribute-defined-outside-init, too-many-locals
# pylint: disable=too-many-instance-attributes, too-many-statements
# pylint: disable=too-many-lines, too-many-branches


class SetupDialog:
    """Dialog to setup the application"""

    # Software widgets ids
    __WIDGET_ID_software = 'software'
    __WIDGET_ID_SOFTWARE_FRAME = 'software_frame'
    __WIDGET_ID_PATH_FRAME = 'path_frame'
    __WIDGET_ID_PATH_LABEL = 'path_label'
    __WIDGET_ID_PATH_VAR = 'path_var'
    __WIDGET_ID_BROWSE_BUTTON = 'browse_button'
    __WIDGET_ID_SOURCE_FRAME = 'source_frame'
    __WIDGET_ID_SOURCE_GAME_INFO_LABEL = 'source_game_info_label'
    __WIDGET_ID_SOURCE_GAME_INFO_COMBO = 'source_game_info_combo'
    __WIDGET_ID_MULTI_FRAME = 'multi_frame'
    __WIDGET_ID_PLATFORM_ASSOCIATIONS_FRAME = 'platform_associations_frame'
    __WIDGET_ID_PLATFORM_ASSOCIATIONS_TABLE = 'platform_associations_table'
    __WIDGET_ID_PLATFORM_ASSOCIATIONS_ADD_BUTTON = 'platform_associations_add_button'
    __WIDGET_ID_PLATFORM_ASSOCIATIONS_REMOVE_BUTTON = 'platform_associations_remove_button'
    __WIDGET_ID_MEDIA_ASSOCIATIONS_FRAME = 'media_associations_frame'
    __WIDGET_ID_MEDIA_ASSOCIATIONS_TABLE = 'media_associations_table'
    __WIDGET_ID_MEDIA_ASSOCIATIONS_ADD_BUTTON = 'media_associations_add_button'
    __WIDGET_ID_MEDIA_ASSOCIATIONS_REMOVE_BUTTON = 'media_associations_remove_button'
    __WIDGET_ID_MEDIA_POSITIONS_FRAME = 'media_positions_frame'
    __WIDGET_ID_MEDIA_POSITIONS_GRID = 'media_positions_grid'

    def __init__(
        self,
        parent,
        callback: any
    ):
        """Initialize dialog"""

        self.__loaded: bool = False
        self.__callback: any = callback
        self.__lang_code: str = Context.get_lang_code()
        self.__software_widgets: dict[SoftwareId, dict[str, tk.Variable]] = {}

        # Create dialog
        self.dialog = UIHelper.create_dialog(parent)

        # Iconify parent and dialog
        parent.withdraw()
        self.dialog.withdraw()

        # Create components
        self.__create_general_components()
        self.__create_platforms_components()
        self.__create_softwares_components()
        self.__create_buttons_components()

        # Update texts in UI Components
        self.__update_ui_components_texts()

        self.__loaded = True

        # Update screen about entry changed
        self.__on_entry_changed(None)

        # Fix dialog's size and position
        UIHelper.center_dialog(
            dialog=self.dialog,
            width=1600,
            height=1245
        )

    def __get_text(
        self,
        text_id: str,
        newline_if_parenthesis: bool = False,
        **kwargs
    ) -> str:
        """Get text from its id using the current lang parameter"""

        result = Context.get_text(
            text_id=text_id,
            lang=self.__lang_code,
            kwargs=kwargs
        )

        if newline_if_parenthesis and result:
            result = re.sub(r"\s*(\([^)]*\))", r"\n\1", result)

        return result

    def __find_media(self, media_text) -> Media:
        """Find media from its text"""

        if not media_text:
            return None

        normalized_text = media_text.replace("\n", " ").strip()
        for media in Media:
            for lang_code in ['fr', 'en']:
                if Context.get_text(
                    media.value,
                    lang=lang_code
                ) == normalized_text:
                    return media

        return None

    def __get_current_software(self):
        """Get current software"""

        current_tab_index = self.notebook.index("current")
        current_tab_text = self.notebook.tab(current_tab_index, "text")
        for software in SoftwareId:
            if software.value == current_tab_text:
                return software
        return None

    def __browse_folder(
        self,
        entry_folder
    ):
        """Browse folder"""

        folder_selected = filedialog.askdirectory(
            parent=self.dialog
        )
        if folder_selected:
            # Clear current text in the entry
            entry_folder.delete(0, tk.END)
            # Insert the selected folder
            entry_folder.insert(0, folder_selected)

    def __add_platform(self):
        """Add platform"""

        # Ask an entry for platform's name
        platform_name = simpledialog.askstring(
            self.__get_text('confirmation'),
            self.__get_text('confirm_add_platform'),
            parent=self.dialog
        )

        if platform_name is None:
            return

        platform_name = platform_name.strip()

        if len(platform_name) == 0:
            return

        # Add the platform if not already exists
        platforms_rows = []
        for row in self.platforms_table.list_rows():
            if row[Constants.UI_TABLE_KEY_COL_NAME].lower().strip() \
                    == platform_name.lower().strip():
                messagebox.showerror(
                    title=self.__get_text('error_title'),
                    message=self.__get_text('error_platform_already_exists'),
                    parent=self.dialog
                )
                return
            platforms_rows.append(row)
        platforms_rows.append({
            Constants.UI_TABLE_KEY_COL_SELECTION: False,
            Constants.UI_TABLE_KEY_COL_ID: platform_name,
            Constants.UI_TABLE_KEY_COL_NAME: platform_name
        })

        # Sort rows by platform name (case-insensitive)
        platforms_rows = sorted(
            platforms_rows,
            key=lambda r: r[Constants.UI_TABLE_KEY_COL_NAME].lower().strip()
        )

        self.platforms_table.set_rows(platforms_rows)

        # Prevent that entry changed
        self.__on_entry_changed()

    def __remove_platform(self):
        """Remove platform"""

        # Ask a confirmation to delete
        if not messagebox.askokcancel(
            self.__get_text('confirmation'),
            self.__get_text(
                'confirm_remove_platforms'
            ),
            parent=self.dialog
        ):
            return

        # Retrieve selected rows
        selected_rows = self.platforms_table.get_selected_rows()

        # Remove all selected rows
        platforms_rows = []
        deleted_platforms = []
        for row in self.platforms_table.list_rows():
            if row in selected_rows:
                deleted_platforms.append(row[Constants.UI_TABLE_KEY_COL_NAME])
                continue
            platforms_rows.append(row)
        self.platforms_table.set_rows(platforms_rows)

        # Remove all platforms associations concerned by the deleted platforms
        for current_software in SoftwareId:
            current_software_widgets = self.__software_widgets[current_software]
            associations_table = current_software_widgets[
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_TABLE
            ]

            platforms_rows = []
            for row in associations_table.list_rows():
                if row[Constants.UI_TABLE_KEY_COL_PLATFORM] in deleted_platforms:
                    continue
                platforms_rows.append(row)
            associations_table.set_rows(platforms_rows)

        # Prevent that entry changed
        self.__on_entry_changed()

    def __add_platform_association(self):
        """Add platform association"""

        # Retrieve software manager and software associations table
        current_software_widgets = self.__software_widgets[self.__get_current_software(
        )]
        software = current_software_widgets[
            SetupDialog.__WIDGET_ID_software
        ]
        associations_table = current_software_widgets[
            SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_TABLE
        ]

        # List associated platforms and folders
        associated_platforms = []
        associated_roms_folders = []
        for row in associations_table.list_rows():
            associated_platforms.append(
                row[Constants.UI_TABLE_KEY_COL_PLATFORM])
            associated_roms_folders.append(
                row[Constants.UI_TABLE_KEY_COL_ROMS_FOLDER])

        # Ask to select a platform without association
        available_platforms = []
        for row in self.platforms_table.list_rows():
            if row[Constants.UI_TABLE_KEY_COL_NAME] in associated_platforms:
                continue
            available_platforms.append(row[Constants.UI_TABLE_KEY_COL_NAME])

        if len(available_platforms) == 0:
            messagebox.showerror(
                title=self.__get_text('error_title'),
                message=self.__get_text('error_all_platforms_associated'),
                parent=self.dialog
            )
            return

        platform_selection_dialog = SelectionDialog(
            parent=self.dialog,
            title=self.__get_text('confirmation'),
            message=self.__get_text('confirm_select_platform'),
            values=available_platforms
        )
        selected_platform = platform_selection_dialog.result

        if selected_platform is None:
            return

        # Ask to select a rom folder without association
        available_roms_folders = []
        for roms_folder in software.list_roms_folders():
            if roms_folder in associated_roms_folders:
                continue
            available_roms_folders.append(roms_folder)

        roms_folder_selection_enabled = len(available_roms_folders) > 0
        if roms_folder_selection_enabled:
            roms_folder_selection_enabled = messagebox.askyesno(
                self.__get_text('question'),
                self.__get_text('question_select_roms_folder'),
                parent=self.dialog
            )

        if roms_folder_selection_enabled:
            if len(available_roms_folders) == 0:
                messagebox.showerror(
                    title=self.__get_text('error_title'),
                    message=self.__get_text(
                        'error_all_roms_folders_associated'
                    ),
                    parent=self.dialog
                )
                return

            roms_folder_selection_dialog = SelectionDialog(
                parent=self.dialog,
                title=self.__get_text('confirmation'),
                message=self.__get_text('confirm_select_roms_folder'),
                values=available_roms_folders
            )
            selected_roms_folder = roms_folder_selection_dialog.result

            if selected_roms_folder is None:
                return
        else:
            selected_roms_folder = simpledialog.askstring(
                self.__get_text('confirmation'),
                self.__get_text('confirm_create_folder'),
                parent=self.dialog
            )

            if selected_roms_folder is None:
                return

            if selected_roms_folder in software.list_roms_folders():
                messagebox.showerror(
                    title=self.__get_text('error_title'),
                    message=self.__get_text(
                        'error_roms_folder_already_exists',
                        folder=selected_roms_folder
                    ),
                    parent=self.dialog
                )
                return

        # Add the association
        associations_rows = associations_table.list_rows()
        associations_rows.append({
            Constants.UI_TABLE_KEY_COL_SELECTION: False,
            Constants.UI_TABLE_KEY_COL_ID: selected_platform,
            Constants.UI_TABLE_KEY_COL_PLATFORM: selected_platform,
            Constants.UI_TABLE_KEY_COL_ROMS_FOLDER: selected_roms_folder
        })

        # Sort rows by platform (case-insensitive)
        associations_rows = sorted(
            associations_rows,
            key=lambda r: r[Constants.UI_TABLE_KEY_COL_PLATFORM].lower(
            ).strip()
        )

        associations_table.set_rows(associations_rows)

        # Prevent that entry changed
        self.__on_entry_changed()

    def __remove_platform_association(self):
        """Remove platform association"""

        # Retrieve associations tables
        current_software_widgets = self.__software_widgets[self.__get_current_software(
        )]
        associations_table = current_software_widgets[
            SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_TABLE
        ]

        # Ask a confirmation to delete
        if not messagebox.askokcancel(
            self.__get_text('confirmation'),
            self.__get_text(
                'confirm_remove_platform_associations'
            ),
            parent=self.dialog
        ):
            return

        # Retrieve selected rows
        selected_rows = associations_table.get_selected_rows()

        # Remove all selected rows
        platforms_rows = []
        for row in associations_table.list_rows():
            if row in selected_rows:
                continue
            platforms_rows.append(row)
        associations_table.set_rows(platforms_rows)

        # Prevent that entry changed
        self.__on_entry_changed()

    def __add_media_association(self):
        """Add media association"""

        # Retrieve software manager and software associations table
        current_software_widgets = self.__software_widgets[self.__get_current_software(
        )]
        software = current_software_widgets[
            SetupDialog.__WIDGET_ID_software
        ]
        associations_table = current_software_widgets[
            SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_TABLE
        ]

        # List associated media and associated resources
        associated_media = []
        associated_resources = []
        for row in associations_table.list_rows():
            associated_media.append(
                row[Constants.UI_TABLE_KEY_COL_MEDIA]
            )
            associated_resources.append(
                row[Constants.UI_TABLE_KEY_COL_RESOURCE]
            )

        # Check if all resources are already associated
        available_resources = []
        for media_resource in software.list_media_resources():
            if media_resource in associated_resources:
                continue
            available_resources.append(media_resource)

        if len(available_resources) == 0:
            messagebox.showerror(
                title=self.__get_text('error_title'),
                message=self.__get_text(
                    'error_all_resources_associated'
                ),
                parent=self.dialog
            )
            return

        # Ask to select a media
        available_media = []
        for media in Media:
            if self.__get_text(media.value) in associated_media:
                continue
            available_media.append(
                self.__get_text(media.value)
            )

        if len(available_media) == 0:
            messagebox.showerror(
                title=self.__get_text('error_title'),
                message=self.__get_text(
                    'error_all_media_associated'
                ),
                parent=self.dialog
            )
            return

        media_selection_dialog = SelectionDialog(
            parent=self.dialog,
            title=self.__get_text('confirmation'),
            message=self.__get_text('confirm_select_media'),
            values=available_media
        )
        selected_media = media_selection_dialog.result

        if selected_media is None:
            return

        # Ask to select a resource without association
        resource_selection_dialog = SelectionDialog(
            parent=self.dialog,
            title=self.__get_text('confirmation'),
            message=self.__get_text('confirm_select_resource'),
            values=available_resources
        )
        selected_resource = resource_selection_dialog.result

        if selected_resource is None:
            return

        # Add the association
        associations_rows = associations_table.list_rows()
        associations_rows.append({
            Constants.UI_TABLE_KEY_COL_SELECTION: False,
            Constants.UI_TABLE_KEY_COL_ID: selected_media,
            Constants.UI_TABLE_KEY_COL_MEDIA: selected_media,
            Constants.UI_TABLE_KEY_COL_RESOURCE: selected_resource
        })

        # Sort rows by media (case-insensitive)
        associations_rows = sorted(
            associations_rows,
            key=lambda r: r[Constants.UI_TABLE_KEY_COL_MEDIA].lower().strip()
        )

        associations_table.set_rows(associations_rows)

        # Prevent that entry changed
        self.__on_entry_changed()

    def __remove_media_association(self):
        """Remove media association"""

        # Retrieve associations tables
        current_software_widgets = self.__software_widgets[self.__get_current_software(
        )]
        associations_table = current_software_widgets[
            SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_TABLE
        ]

        # Ask a confirmation to delete
        if not messagebox.askokcancel(
            self.__get_text('confirmation'),
            self.__get_text(
                'confirm_remove_media_associations'
            ),
            parent=self.dialog
        ):
            return

        # Retrieve selected rows
        selected_rows = associations_table.get_selected_rows()

        # Remove all selected rows
        removed_media = []
        media_rows = []
        for row in associations_table.list_rows():
            if row in selected_rows:
                removed_media.append(
                    row[Constants.UI_TABLE_KEY_COL_MEDIA]
                )
                continue
            media_rows.append(row)
        associations_table.set_rows(media_rows)

        # Retrieve positions grid
        positions_grid = current_software_widgets[
            SetupDialog.__WIDGET_ID_MEDIA_POSITIONS_GRID
        ]

        # Reinitialize buttons where removed media are positioned
        for position_button in positions_grid.list_buttons():
            found_media = self.__find_media(
                media_text=position_button.cget("text")
            )
            if found_media is None:
                continue
            if self.__get_text(found_media.value) not in removed_media:
                continue
            position_button.configure(
                text=' '
            )

        # Prevent that entry changed
        self.__on_entry_changed()

    def __validate(self):
        """Validate"""

        # Retrieve general setup
        monitor = int(self.combo_monitor.get()) - 1
        simulated = self.simulation_boolean_var.get()

        setup = {}

        # Set general setup
        general_setup = {}
        general_setup[Constants.SETUP_TAG_LANG_CODE] = self.__lang_code
        general_setup[Constants.SETUP_TAG_MONITOR] = monitor
        general_setup[Constants.SETUP_TAG_SIMULATED] = simulated
        setup[Constants.SETUP_TAG_GENERAL] = general_setup

        # Set platforms
        platforms = []
        for row in self.platforms_table.list_rows():
            platforms.append(row[Constants.UI_TABLE_KEY_COL_NAME])
        setup[Constants.SETUP_TAG_PLATFORMS] = platforms

        # Set softwares setup
        setup[Constants.SETUP_TAG_SOFTWARES] = []
        for software, widgets in self.__software_widgets.items():

            # Initialize setup for software
            software_config = {
                Constants.SETUP_TAG_ID: software.name
            }
            setup[Constants.SETUP_TAG_SOFTWARES].append(
                software_config
            )

            # Set setup for the software
            software_config[Constants.SETUP_TAG_ENABLED] = len(widgets[
                SetupDialog.__WIDGET_ID_PATH_VAR
            ].get()) > 0
            software_config[Constants.SETUP_TAG_PATH] = widgets[
                SetupDialog.__WIDGET_ID_PATH_VAR
            ].get()

            # Remove all tags if disabled
            if not software_config[Constants.SETUP_TAG_ENABLED]:
                software_config[Constants.SETUP_TAG_SOURCES] = []
                software_config[Constants.SETUP_TAG_PLATFORM_ASSOCIATIONS] = []
                software_config[Constants.SETUP_TAG_MEDIA_ASSOCIATIONS] = []
                software_config[Constants.SETUP_TAG_MEDIA_POSITIONS] = []
                continue

            # Set sources
            sources = []
            source_software = None
            for source_software in SoftwareId:
                if source_software.value != widgets[
                    SetupDialog.__WIDGET_ID_SOURCE_GAME_INFO_COMBO
                ].get():
                    continue
                sources.append({
                    Constants.SETUP_TAG_ID: Constants.SETUP_SOURCE_GAME_INFO,
                    Constants.SETUP_TAG_SOFTWARE: source_software.name
                })
                break
            software_config[Constants.SETUP_TAG_SOURCES] = sources

            # Set platform associations
            platform_associations_table = widgets[
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_TABLE
            ]
            platform_associations = []
            for row in platform_associations_table.list_rows():
                platform_associations.append({
                    Constants.SETUP_TAG_PLATFORM: row[Constants.UI_TABLE_KEY_COL_PLATFORM],
                    Constants.SETUP_TAG_ROMS_FOLDER: row[Constants.UI_TABLE_KEY_COL_ROMS_FOLDER]
                })
            software_config[Constants.SETUP_TAG_PLATFORM_ASSOCIATIONS] = platform_associations

            # Set media associations
            media_associations_table = widgets[
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_TABLE
            ]
            media_associations = []
            for row in media_associations_table.list_rows():
                media_associations.append({
                    Constants.SETUP_TAG_MEDIA: self.__find_media(
                        media_text=row[Constants.UI_TABLE_KEY_COL_MEDIA]
                    ).name,
                    Constants.SETUP_TAG_RESOURCE: row[Constants.UI_TABLE_KEY_COL_RESOURCE]
                })
            software_config[Constants.SETUP_TAG_MEDIA_ASSOCIATIONS] = media_associations

            # Set media positions
            media_positions_grid = widgets[
                SetupDialog.__WIDGET_ID_MEDIA_POSITIONS_GRID
            ]
            media_positions = []
            for row in range(media_positions_grid.rows):
                for column in range(media_positions_grid.columns):
                    found_media = self.__find_media(
                        media_text=media_positions_grid.get_button(
                            row=row,
                            column=column
                        ).cget("text")
                    )
                    if found_media is None:
                        continue
                    media_positions.append({
                        Constants.SETUP_TAG_MEDIA: found_media.name,
                        Constants.SETUP_TAG_ROW: row,
                        Constants.SETUP_TAG_COLUMN: column
                    })
            software_config[Constants.SETUP_TAG_MEDIA_POSITIONS] = media_positions

        # Save set to XML
        XmlHelper.save_xml(
            xml_file_path=Context.get_setup_file_path(),
            root_tag=Constants.SETUP_TAG_ROOT,
            obj=setup,
            force=True
        )

        # Close the dialog after validation
        UIHelper.close_dialog(self.dialog)

        # Call back
        self.__callback()

    def __cancel(self):
        """Cancel"""

        # Close the dialog without saving
        UIHelper.close_dialog(self.dialog)

    def __update_platforms_buttons(self, *_):
        """Update platforms buttons"""

        # Enable/Disable buttons for the button to remove
        if len(self.platforms_table.get_selected_rows()) >= 1:
            self.remove_platforms_button.config(state=tk.NORMAL)
        else:
            self.remove_platforms_button.config(state=tk.DISABLED)

    def __update_platform_associations_buttons(self, *_):
        """Update platform associations buttons"""

        # Retrieve software associations table and associations remove button
        current_software_widgets = self.__software_widgets[self.__get_current_software(
        )]
        platform_associations_table = current_software_widgets[
            SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_TABLE
        ]
        platform_associations_remove_button = current_software_widgets[
            SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_REMOVE_BUTTON
        ]

        # Enable/Disable buttons for the button to remove
        if len(platform_associations_table.get_selected_rows()) >= 1:
            platform_associations_remove_button.config(
                state=tk.NORMAL
            )
        else:
            platform_associations_remove_button.config(
                state=tk.DISABLED
            )

    def __update_media_associations_buttons(self, *_):
        """Update media associations buttons"""

        # Retrieve software associations table and associations remove button
        current_software_widgets = self.__software_widgets[self.__get_current_software(
        )]
        media_associations_table = current_software_widgets[
            SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_TABLE
        ]
        media_associations_remove_button = current_software_widgets[
            SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_REMOVE_BUTTON
        ]

        # Enable/Disable buttons for the button to remove
        if len(media_associations_table.get_selected_rows()) >= 1:
            media_associations_remove_button.config(
                state=tk.NORMAL
            )
        else:
            media_associations_remove_button.config(
                state=tk.DISABLED
            )

    def __on_button_position_clicked(self, button_grid: UIButtonGrid, row: int, column: int):
        """Called when button position clicked"""

        # Try to find the media
        found_media = self.__find_media(
            media_text=button_grid.get_button(
                row=row,
                column=column
            ).cget("text")
        )

        if found_media is None:

            # Retrieve software associations table and associations remove button
            current_software_widgets = self.__software_widgets[self.__get_current_software(
            )]
            media_associations_table = current_software_widgets[
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_TABLE
            ]

            # List associated media and associated resources
            associated_media = []
            for table_row in media_associations_table.list_rows():
                associated_media.append(
                    table_row[Constants.UI_TABLE_KEY_COL_MEDIA]
                )

            # List positioned media
            positioned_media = []
            for position_button in button_grid.list_buttons():
                found_media = self.__find_media(
                    media_text=position_button.cget("text")
                )

                if found_media is None:
                    continue

                positioned_media.append(self.__get_text(
                    found_media.value
                ))

            # Ask to select a media
            available_media = []
            for media in associated_media:
                if media in positioned_media:
                    continue
                available_media.append(media)

            if len(available_media) == 0:
                messagebox.showerror(
                    title=self.__get_text('error_title'),
                    message=self.__get_text(
                        'error_all_media_positioned'
                    ),
                    parent=self.dialog
                )
                return

            media_selection_dialog = SelectionDialog(
                parent=self.dialog,
                title=self.__get_text('confirmation'),
                message=self.__get_text('confirm_select_media'),
                values=available_media
            )
            selected_media = media_selection_dialog.result

            if selected_media is None:
                return

            new_text = self.__get_text(
                text_id=self.__find_media(
                    media_text=selected_media
                ).value,
                newline_if_parenthesis=True
            )
        else:
            # Else, reinitialize the button's text
            new_text = ' '

        button_grid.get_button(
            row=row,
            column=column
        ).configure(
            text=new_text
        )

        # Prevent that entry changed
        self.__on_entry_changed()

    def __on_entry_changed(self, *args):
        """Called when an entry changed"""

        if not self.__loaded:
            return

        # Try to retrieve the event widget
        try:
            event_widget = args[0].widget
        except Exception:
            try:
                event_widget = args[0]
            except Exception:
                event_widget = None

        # Reload UI Texts if the source is the combo lang
        if event_widget == self.combo_lang:
            self.__lang_code = 'en'
            if self.combo_lang.get() == self.__get_text('lang_fr'):
                self.__lang_code = 'fr'

            # Update texts in UI Components
            self.__update_ui_components_texts()

        # Show/Hide components for softwares
        for software, widgets in self.__software_widgets.items():

            # Ignore if not the enable widget
            if event_widget is not None and \
                    str(widgets[SetupDialog.__WIDGET_ID_PATH_VAR]) != str(event_widget):
                continue

            # If software path modified, update the software manager
            if str(widgets[SetupDialog.__WIDGET_ID_PATH_VAR]) == str(event_widget):
                widgets[
                    SetupDialog.__WIDGET_ID_software
                ] = AbstractSoftware.get_registered_software(
                    software_id=software
                )

            # Retrieve frames to hide/show
            software_source_frame = widgets[SetupDialog.__WIDGET_ID_SOURCE_FRAME]
            software_multi_frame = widgets[
                SetupDialog.__WIDGET_ID_MULTI_FRAME]

            # Hide the frames by default
            software_source_frame.pack_forget()
            software_multi_frame.pack_forget()

            # Show the frames if software is path is not empty
            if len(widgets[SetupDialog.__WIDGET_ID_PATH_VAR].get()) > 0:
                software_source_frame.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    padx=Constants.UI_PAD_SMALL,
                    pady=Constants.UI_PAD_SMALL
                )

                software_multi_frame.pack(
                    side=tk.TOP,
                    fill=tk.X,
                    padx=Constants.UI_PAD_SMALL,
                    pady=Constants.UI_PAD_SMALL
                )

        # Enable/Disable button to validate
        validate_enabled = len(self.platforms_table.list_rows()) > 0
        available_softwares_counter = 0
        for widgets in self.__software_widgets.values():
            if len(widgets[SetupDialog.__WIDGET_ID_PATH_VAR].get()) == 0:
                continue

            available_softwares_counter += 1

            # Retrieve platform associations
            platform_associations_table = widgets[
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_TABLE
            ]
            if len(platform_associations_table.list_rows()) == 0:
                validate_enabled = False

            # Retrieve media associations
            media_associations_table = widgets[
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_TABLE
            ]
            if len(media_associations_table.list_rows()) == 0:
                validate_enabled = False

            # Retrieve if positioned media
            media_positions_grid = widgets[
                SetupDialog.__WIDGET_ID_MEDIA_POSITIONS_GRID
            ]
            positioned_media = False
            for row in range(media_positions_grid.rows):
                for column in range(media_positions_grid.columns):
                    found_media = self.__find_media(
                        media_text=media_positions_grid.get_button(
                            row=row,
                            column=column
                        ).cget("text")
                    )
                    if found_media is None:
                        continue
                    positioned_media = True
                    break
            if not positioned_media:
                validate_enabled = False

        # Can't validate if no available softwares
        if available_softwares_counter == 0:
            validate_enabled = False

        if validate_enabled:
            self.button_validate.config(state=tk.NORMAL)
        else:
            self.button_validate.config(state=tk.DISABLED)

    def __create_general_components(self):
        """Create general components"""

        # Create frame
        self.general_frame = tk.LabelFrame(
            self.dialog
        )
        self.general_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_SMALL
        )

        # Create Combobox for language
        lang_frame = tk.Frame(self.general_frame)
        lang_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            pady=Constants.UI_PAD_SMALL
        )
        self.label_lang = tk.Label(
            lang_frame
        )
        self.label_lang.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_lang = ttk.Combobox(
            lang_frame,
            values=[]
        )
        self.combo_lang.config(state="readonly")
        self.combo_lang.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_lang.bind(
            "<<ComboboxSelected>>",
            self.__on_entry_changed
        )

        # Create Combobox for monitor
        monitor_frame = tk.Frame(self.general_frame)
        monitor_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            pady=Constants.UI_PAD_SMALL
        )
        self.label_monitor = tk.Label(
            monitor_frame
        )
        self.label_monitor.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_monitor = ttk.Combobox(
            monitor_frame,
            values=list(range(1, UIHelper.count_monitors() + 1))
        )
        self.combo_monitor.set(
            Context.get_monitor() + 1
        )
        self.combo_monitor.config(state="readonly")
        self.combo_monitor.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_monitor.bind(
            "<<ComboboxSelected>>",
            self.__on_entry_changed
        )

        # Create simulation checkbox
        simulation_frame = tk.Frame(self.general_frame)
        simulation_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.simulation_boolean_var = tk.BooleanVar()
        self.simulation_boolean_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.simulation_boolean_var.set(
            Context.is_simulated()
        )
        simulation_checkbox = tk.Checkbutton(
            simulation_frame,
            variable=self.simulation_boolean_var
        )
        simulation_checkbox.pack(
            side=tk.LEFT,
        )
        self.label_simulation = tk.Label(
            simulation_frame
        )
        self.label_simulation.pack(
            side=tk.LEFT
        )
        self.label_simulation.bind(
            "<Button-1>",
            lambda e: simulation_checkbox.invoke()
        )

    def __create_platforms_components(self):
        """Create softwares components"""

        # Create frame
        self.platforms_frame = tk.LabelFrame(
            self.dialog
        )
        self.platforms_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_SMALL
        )

        # Add a table for platforms
        table_frame = tk.Frame(
            self.platforms_frame
        )
        table_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH
        )
        platforms_rows = []
        for platform in Context.list_available_platforms():
            platforms_rows.append({
                Constants.UI_TABLE_KEY_COL_SELECTION: False,
                Constants.UI_TABLE_KEY_COL_ID: platform,
                Constants.UI_TABLE_KEY_COL_NAME: platform
            })
        if len(platforms_rows) == 0:
            for platform in Constants.DEFAULT_PLATFORMS:
                platforms_rows.append({
                    Constants.UI_TABLE_KEY_COL_SELECTION: False,
                    Constants.UI_TABLE_KEY_COL_ID: platform,
                    Constants.UI_TABLE_KEY_COL_NAME: platform
                })

        self.platforms_table = UITable(
            parent=table_frame,
            rows=platforms_rows,
            multiple_selection=True,
            actions_buttons_factory=self.__create_platforms_actions_buttons,
            on_selected_rows_change=self.__update_platforms_buttons
        )

    def __create_platforms_actions_buttons(self, master: tk.Misc) -> list[tk.Button]:
        """Create actions buttons for platforms"""

        self.add_platform_button = tk.Button(
            master,
            command=self.__add_platform
        )
        self.remove_platforms_button = tk.Button(
            master,
            state=tk.DISABLED,
            command=self.__remove_platform
        )
        return [
            self.add_platform_button,
            self.remove_platforms_button
        ]

    def __create_softwares_components(self):
        """Create softwares components"""

        # Create frame
        self.softwares_frame = tk.LabelFrame(
            self.dialog
        )
        self.softwares_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_SMALL
        )

        # Create a notebook
        self.notebook = ttk.Notebook(self.softwares_frame)
        self.notebook.pack(
            expand=True,
            fill=tk.BOTH,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )

        # Add a tab for each software
        for current_software in SoftwareId:
            # Create the software manager
            software = AbstractSoftware.get_registered_software(
                software_id=current_software
            )

            # Create the software's tab
            software_frame = ttk.Frame(self.notebook)
            self.notebook.add(
                software_frame,
                text=current_software.value
            )

            # Retrieve the software context
            software_context = None
            if len(Context.list_available_softwares()) > 0:
                software_context = Context.get_software_context(
                    software_id=current_software
                )

            # Add a frame to select the software's path
            software_path_frame = tk.Frame(
                software_frame
            )
            software_path_frame.pack(
                side=tk.TOP,
                fill=tk.X,
                padx=Constants.UI_PAD_SMALL,
                pady=Constants.UI_PAD_SMALL
            )
            software_path_label = tk.Label(
                software_path_frame,
            )
            software_path_label.pack(
                side=tk.LEFT,
                padx=Constants.UI_PAD_SMALL
            )
            software_path_var = tk.StringVar()
            software_path_var.trace_add(
                "write",
                self.__on_entry_changed
            )
            software_path_entry = tk.Entry(
                software_path_frame,
                textvariable=software_path_var,
                width=40
            )
            software_path_entry.insert(
                0,
                '' if software_context is None else software_context.path
            )
            software_path_entry.pack(
                side=tk.LEFT,
                padx=Constants.UI_PAD_SMALL
            )
            software_browse_button = tk.Button(
                software_path_frame,
                command=lambda entry=software_path_entry: self.__browse_folder(
                    entry
                )
            )
            software_browse_button.pack(
                side=tk.LEFT,
                padx=Constants.UI_PAD_SMALL
            )

            # Add a combobox to define the source for description
            software_source_frame = tk.Frame(
                software_frame
            )
            software_source_game_info_label = tk.Label(
                software_source_frame,
            )
            software_source_game_info_label.pack(
                side=tk.LEFT,
                padx=Constants.UI_PAD_SMALL
            )
            source_softwares = []
            for source_software in SoftwareId:
                source_softwares.append(source_software.value)
            software_source_game_info_combo = ttk.Combobox(
                software_source_frame,
                width=15,
                values=source_softwares
            )
            software_source_game_info_combo.pack(
                side=tk.LEFT,
                padx=Constants.UI_PAD_SMALL
            )
            software_source_game_info_combo.config(state="readonly")
            software_source_game_info_combo.set(
                current_software.value
            )
            software_source_game_info_combo.bind(
                "<<ComboboxSelected>>",
                self.__on_entry_changed
            )
            if software_context is not None and software_context.enabled:
                software_source_game_info_combo.set(
                    software_context.sources[Constants.SETUP_SOURCE_GAME_INFO].value
                )

            # Create left frame and right frame
            multi_frame = tk.Frame(
                software_frame
            )
            left_frame = tk.Frame(
                multi_frame
            )
            left_frame.pack(
                side=tk.LEFT,
                fill=tk.X,
                expand=True
            )
            right_frame = tk.Frame(
                multi_frame
            )
            right_frame.pack(
                side=tk.RIGHT,
                fill=tk.BOTH
            )

            # Retrieve the platform associations from default
            platform_associations = {}
            for platform, roms_folder in software.get_default_platform_associations().items():
                for row in self.platforms_table.list_rows():
                    if row[Constants.UI_TABLE_KEY_COL_NAME] != platform:
                        continue
                    platform_associations[platform] = roms_folder
                    break

            # Retrieve the platform associations from config if possible
            if software_context is not None and software_context.enabled:
                platform_associations = software_context.platform_associations

            # Add table for platform associations
            platform_associations_frame = tk.LabelFrame(
                left_frame
            )
            platform_associations_frame.pack(
                side=tk.TOP,
                fill=tk.X,
                padx=Constants.UI_PAD_SMALL,
                pady=Constants.UI_PAD_SMALL
            )
            platform_associations_table_frame = tk.Frame(
                platform_associations_frame
            )
            platform_associations_table_frame.pack(
                side=tk.TOP,
                fill=tk.BOTH
            )
            platform_associations_table_rows = []
            for platform, roms_folder in platform_associations.items():
                platform_associations_table_rows.append({
                    Constants.UI_TABLE_KEY_COL_SELECTION: False,
                    Constants.UI_TABLE_KEY_COL_ID: platform,
                    Constants.UI_TABLE_KEY_COL_PLATFORM: platform,
                    Constants.UI_TABLE_KEY_COL_ROMS_FOLDER: roms_folder
                })

            # Sort rows by platform (case-insensitive)
            platform_associations_table_rows = sorted(
                platform_associations_table_rows,
                key=lambda r: r[Constants.UI_TABLE_KEY_COL_PLATFORM].lower(
                ).strip()
            )

            platform_associations_table = UITable(
                parent=platform_associations_table_frame,
                rows=platform_associations_table_rows,
                multiple_selection=True,
                actions_buttons_factory=self.__create_platform_associations_actions_buttons,
                on_selected_rows_change=self.__update_platform_associations_buttons
            )

            # Retrieve the media associations from default
            media_associations = software.get_default_media_associations()

            # Retrieve the media associations from config if possible
            if software_context is not None and software_context.enabled:
                media_associations = software_context.media_associations

            # Add table for media associations
            media_associations_frame = tk.LabelFrame(
                left_frame
            )
            media_associations_frame.pack(
                side=tk.TOP,
                fill=tk.X,
                padx=Constants.UI_PAD_SMALL,
                pady=Constants.UI_PAD_SMALL
            )
            media_associations_table_frame = tk.Frame(
                media_associations_frame
            )
            media_associations_table_frame.pack(
                side=tk.TOP,
                fill=tk.BOTH
            )
            media_associations_table_rows = []
            for media, resource in media_associations.items():
                media_associations_table_rows.append(
                    {
                        Constants.UI_TABLE_KEY_COL_SELECTION: False,
                        Constants.UI_TABLE_KEY_COL_ID: media.value,
                        Constants.UI_TABLE_KEY_COL_MEDIA: self.__get_text(
                            media.value
                        ),
                        Constants.UI_TABLE_KEY_COL_RESOURCE: resource
                    }
                )

            # Sort rows by media (case-insensitive)
            media_associations_table_rows = sorted(
                media_associations_table_rows,
                key=lambda r: r[Constants.UI_TABLE_KEY_COL_MEDIA].lower(
                ).strip()
            )

            media_associations_table = UITable(
                parent=media_associations_table_frame,
                rows=media_associations_table_rows,
                multiple_selection=True,
                actions_buttons_factory=self.__create_media_associations_actions_buttons,
                on_selected_rows_change=self.__update_media_associations_buttons
            )

            # Retrieve the media positions from default
            media_positions = software.get_default_media_positions()

            # Retrieve the media positions from config if possible
            if software_context is not None and software_context.enabled:
                media_positions = software_context.media_positions

            # Add a grid for media positions
            media_positions_frame = tk.LabelFrame(
                right_frame
            )
            media_positions_frame.pack(
                side=tk.TOP,
                fill=tk.X,
                padx=Constants.UI_PAD_SMALL,
                pady=Constants.UI_PAD_SMALL
            )
            media_positions_grid = UIButtonGrid(
                parent=media_positions_frame,
                rows=5,
                columns=5,
                cell_width=100,
                cell_height=100,
                action=self.__on_button_position_clicked
            )
            media_positions_grid.pack()

            # Update buttons from media positions
            for row in range(media_positions_grid.rows):
                for column in range(media_positions_grid.columns):
                    found_media = media_positions.get(
                        (row, column), None)
                    if not found_media:
                        continue
                    position_button = media_positions_grid.get_button(
                        row=row,
                        column=column
                    )
                    position_button.configure(
                        text=self.__get_text(
                            found_media.value,
                            newline_if_parenthesis=True
                        )
                    )

            # Store widgets for the software
            self.__software_widgets[current_software] = {
                SetupDialog.__WIDGET_ID_software: software,
                SetupDialog.__WIDGET_ID_SOFTWARE_FRAME: software_frame,
                SetupDialog.__WIDGET_ID_PATH_FRAME: software_path_frame,
                SetupDialog.__WIDGET_ID_PATH_LABEL: software_path_label,
                SetupDialog.__WIDGET_ID_PATH_VAR: software_path_var,
                SetupDialog.__WIDGET_ID_BROWSE_BUTTON: software_browse_button,
                SetupDialog.__WIDGET_ID_SOURCE_FRAME: software_source_frame,
                SetupDialog.__WIDGET_ID_SOURCE_GAME_INFO_LABEL: software_source_game_info_label,
                SetupDialog.__WIDGET_ID_SOURCE_GAME_INFO_COMBO: software_source_game_info_combo,
                SetupDialog.__WIDGET_ID_MULTI_FRAME: multi_frame,
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_FRAME: platform_associations_frame,
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_ADD_BUTTON:
                platform_associations_table.get_actions_buttons()[0],
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_REMOVE_BUTTON:
                platform_associations_table.get_actions_buttons()[1],
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_TABLE: platform_associations_table,
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_FRAME: media_associations_frame,
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_ADD_BUTTON:
                media_associations_table.get_actions_buttons()[0],
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_REMOVE_BUTTON:
                media_associations_table.get_actions_buttons()[1],
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_TABLE: media_associations_table,
                SetupDialog.__WIDGET_ID_MEDIA_POSITIONS_FRAME: media_positions_frame,
                SetupDialog.__WIDGET_ID_MEDIA_POSITIONS_GRID: media_positions_grid
            }

    def __create_platform_associations_actions_buttons(self, master: tk.Misc) -> list[tk.Button]:
        """Create actions buttons for platform associations"""

        software_add_button = tk.Button(
            master,
            command=self.__add_platform_association
        )
        software_remove_button = tk.Button(
            master,
            state=tk.DISABLED,
            command=self.__remove_platform_association
        )
        return [
            software_add_button,
            software_remove_button
        ]

    def __create_media_associations_actions_buttons(self, master: tk.Misc) -> list[tk.Button]:
        """Create actions buttons for media associations"""

        software_add_button = tk.Button(
            master,
            command=self.__add_media_association
        )
        software_remove_button = tk.Button(
            master,
            state=tk.DISABLED,
            command=self.__remove_media_association
        )
        return [
            software_add_button,
            software_remove_button
        ]

    def __create_buttons_components(self):
        """Create bottom components"""

        # Create buttons frame
        buttons_frame = tk.Frame(
            self.dialog
        )
        buttons_frame.pack(
            side=tk.BOTTOM,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )

        # Create buttons to cancel and validate
        self.button_cancel = tk.Button(
            buttons_frame,
            command=self.__cancel
        )
        self.button_cancel.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )

        self.button_validate = tk.Button(
            buttons_frame,
            state=tk.DISABLED,
            command=self.__validate
        )
        self.button_validate.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

    def __update_ui_components_texts(self):
        """Update texts in UI Components"""

        self.dialog.title(self.__get_text(
            'setup'
        ))

        self.label_lang.config(
            text=self.__get_text(
                'lang'
            )
        )

        self.combo_lang.config(
            values=[
                self.__get_text(
                    'lang_fr'
                ),
                self.__get_text(
                    'lang_en'
                )
            ]
        )
        self.combo_lang.set(
            self.__get_text(
                f'lang_{self.__lang_code}'
            )
        )

        self.general_frame.config(
            text=self.__get_text(
                'setup_general'
            )
        )

        self.label_monitor.config(
            text=self.__get_text(
                'monitor'
            )
        )

        self.label_simulation.config(
            text=self.__get_text(
                'simulation'
            )
        )

        self.platforms_frame.config(
            text=self.__get_text(
                'setup_platforms'
            )
        )

        self.add_platform_button.config(
            text=self.__get_text(
                'setup_add'
            )
        )

        self.remove_platforms_button.config(
            text=self.__get_text(
                'setup_remove'
            )
        )

        # Update labels for softwares
        for current_software in SoftwareId:
            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_PATH_LABEL].config(
                text=self.__get_text(
                    'setup_folder'
                )
            )

            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_BROWSE_BUTTON].config(
                text=self.__get_text(
                    'setup_browse'
                )
            )

            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_FRAME].config(
                text=self.__get_text(
                    'setup_platform_associations'
                )
            )

            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_SOURCE_GAME_INFO_LABEL].config(
                text=self.__get_text(
                    'setup_source_game_info'
                )
            )

            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_ADD_BUTTON].config(
                text=self.__get_text(
                    'setup_add'
                )
            )

            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_PLATFORM_ASSOCIATIONS_REMOVE_BUTTON].config(
                text=self.__get_text(
                    'setup_remove'
                )
            )

            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_FRAME].config(
                text=self.__get_text(
                    'setup_media_associations'
                )
            )

            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_ADD_BUTTON].config(
                text=self.__get_text(
                    'setup_add'
                )
            )

            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_REMOVE_BUTTON].config(
                text=self.__get_text(
                    'setup_remove'
                )
            )

            self.__software_widgets[current_software][
                SetupDialog.__WIDGET_ID_MEDIA_POSITIONS_FRAME].config(
                text=self.__get_text(
                    'setup_media_positions'
                )
            )

            # Retrieve media associations tables
            current_software_widgets = self.__software_widgets[current_software]
            media_associations_table = current_software_widgets[
                SetupDialog.__WIDGET_ID_MEDIA_ASSOCIATIONS_TABLE
            ]

            # Update media in all media associations
            media_rows = []
            for row in media_associations_table.list_rows():
                media_rows.append({
                    Constants.UI_TABLE_KEY_COL_SELECTION: row[
                        Constants.UI_TABLE_KEY_COL_SELECTION
                    ],
                    Constants.UI_TABLE_KEY_COL_ID: row[
                        Constants.UI_TABLE_KEY_COL_ID
                    ],
                    Constants.UI_TABLE_KEY_COL_MEDIA: self.__get_text(
                        self.__find_media(
                            media_text=row[Constants.UI_TABLE_KEY_COL_MEDIA]
                        ).value
                    ),
                    Constants.UI_TABLE_KEY_COL_RESOURCE: row[
                        Constants.UI_TABLE_KEY_COL_RESOURCE
                    ]
                })
            media_associations_table.set_rows(media_rows)

            # Retrieve media positions grid
            media_positions_grid = current_software_widgets[
                SetupDialog.__WIDGET_ID_MEDIA_POSITIONS_GRID
            ]

            # Update media in all media positions
            for position_button in media_positions_grid.list_buttons():
                found_media = self.__find_media(
                    media_text=position_button.cget("text")
                )
                if found_media is None:
                    continue
                position_button.configure(
                    text=self.__get_text(
                        found_media.value,
                        newline_if_parenthesis=True
                    )
                )

        self.softwares_frame.config(
            text=self.__get_text(
                'setup_softwares'
            )
        )

        self.button_cancel.config(
            text=self.__get_text(
                'cancel'
            )
        )

        self.button_validate.config(
            text=self.__get_text(
                'validate'
            )
        )
