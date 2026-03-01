# pylint: disable=invalid-name
#!/usr/bin/python3
"""Application to manage my Retrobox"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from dialogs.about.about_dialog import AboutDialog
from dialogs.editor.configs_files_editor_dialog import ConfigsFilesEditorDialog
from dialogs.editor.configs_regedit_editor_dialog import ConfigsRegistryEditorDialog
from dialogs.editor.media_editor_dialog import MediaEditorDialog
from dialogs.execute.execute_dialog import ExecuteDialog
from dialogs.refresh.refresh_dialog import RefreshDialog
from dialogs.setup.setup_dialog import SetupDialog
from libraries.file.file_helper import FileHelper
from libraries.constants.constants import Action, Category, Component, Constants, SoftwareId
from libraries.context.context import Context
from libraries.ui.ui_helper import UIHelper
from libraries.ui.ui_table import UITable
from libraries.xml.xml_helper import XmlHelper
from software.abstract_software import AbstractSoftware
from software.batocera.batocera import Batocera
from software.launchbox.launchbox import Launchbox
from software.emu_movies.emu_movies import EmuMovies
from software.skraper.skraper import Skraper

# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-locals


class ApplicationWindow:
    """Application to manage Retrobox"""

    def __init__(self):
        # ---------- Mapping SoftwareId -> Concrete Class ----------
        software_classes = {
            SoftwareId.BATOCERA: Batocera,
            SoftwareId.LAUNCHBOX: Launchbox,
            SoftwareId.EMU_MOVIES: EmuMovies,
            SoftwareId.SKRAPER: Skraper
        }

        # ---------- Register all softwares ----------
        for software_id, cls in software_classes.items():
            AbstractSoftware.register_software(software_id, cls)

        # Initialize selected ids
        self.selected_ids = []

    def __on_selected_rows_changed(self):
        """Called when selected rows changed"""

        # Retrieve selected rows
        selected_top_rows = self.table_top.get_selected_rows()
        selected_bottom_rows = self.table_bottom.get_selected_rows()

        # Update selected ids
        self.selected_ids = self.table_top.get_selected_ids()

        # Enable/Disable buttons for the button to remove
        if len(selected_top_rows) > 0:
            self.refresh_selection_button.config(state=tk.NORMAL)
        else:
            self.refresh_selection_button.config(state=tk.DISABLED)

        # Update execute button state
        if len(selected_top_rows) > 0 and len(selected_bottom_rows) > 0:
            self.button_execute.config(state=tk.NORMAL)
        else:
            # Authorize edit if no rows in top
            if len(selected_bottom_rows) > 0 and Context.get_selected_action() in [
                Action.EDIT
            ]:
                self.button_execute.config(state=tk.NORMAL)
            else:
                self.button_execute.config(state=tk.DISABLED)

    def __on_combo_changed(self, event):
        """Called when a combo changed"""

        # If source is category
        if event.widget == self.combo_category:
            # Update context from selection
            Context.set_selected_category(None)
            for category in Category:
                if Context.get_text(
                    text_id=category.value
                ) == self.combo_category.get():
                    Context.set_selected_category(category)

            # Set title for table
            self.table_top_frame.config(
                text=Context.get_text(
                    Context.get_selected_category().value
                )
            )

            # Update actions depending on selected category
            available_actions = []
            match(Context.get_selected_category()):
                case Category.GAMES:
                    available_actions = [
                        Action.INSTALL,
                        Action.UNINSTALL,
                        Action.EXPORT,
                        Action.VIEW,
                        Action.COPY,
                        Action.EDIT,
                        Action.DELETE
                    ]

                case Category.PLATFORMS:
                    available_actions = [
                        Action.INSTALL,
                        Action.UNINSTALL,
                        Action.EXPORT,
                        Action.COPY,
                        Action.DELETE
                    ]

                case Category.CONFIGS:
                    available_actions = [
                        Action.INSTALL,
                        Action.UNINSTALL,
                        Action.EDIT,
                        Action.DELETE
                    ]

            category_actions = []
            for action in Action:
                if action not in available_actions:
                    continue
                category_actions.append(Context.get_text(
                    action.value,
                    category=Context.get_text(
                        Context.get_selected_category().value
                    )
                ))
            self.combo_action.configure(
                values=category_actions
            )

            # Select first action
            self.combo_action.current(0)
            self.combo_action.event_generate("<<ComboboxSelected>>")

        # If source is action
        elif event.widget == self.combo_action:
            # Update context from selection
            Context.set_selected_action(None)
            for action in Action:
                if Context.get_text(
                    text_id=action.value,
                    category=Context.get_text(
                        Context.get_selected_category().value
                    )
                ) == self.combo_action.get():
                    Context.set_selected_action(action)

            # Show/Hide combos depending on selected category and action
            self.label_software.pack_forget()
            self.combo_software.pack_forget()
            self.label_platform.pack_forget()
            self.combo_platform.pack_forget()
            if Context.get_selected_category() == Category.GAMES:
                if Context.get_selected_action() not in [Action.COPY, Action.DELETE, Action.EDIT]:
                    self.label_software.pack(
                        side=tk.LEFT,
                        padx=Constants.UI_PAD_SMALL
                    )
                    self.combo_software.pack(
                        side=tk.LEFT,
                        padx=Constants.UI_PAD_SMALL
                    )
                self.label_platform.pack(
                    side=tk.LEFT,
                    padx=Constants.UI_PAD_SMALL
                )
                self.combo_platform.pack(
                    side=tk.LEFT,
                    padx=Constants.UI_PAD_SMALL
                )
                if Context.get_selected_action() not in [Action.COPY, Action.DELETE, Action.EDIT]:
                    self.combo_software.current(0)
                    self.combo_software.event_generate("<<ComboboxSelected>>")
                else:
                    # Update platforms
                    values = []
                    for platform in FileHelper.list_sub_directories(
                        folder_path=Context.get_games_path()
                    ):
                        values.append(platform)
                    values.sort()
                    self.combo_platform.configure(
                        values=values
                    )

                    self.combo_platform.current(0)
                    self.combo_platform.event_generate("<<ComboboxSelected>>")
            elif Context.get_selected_category() == Category.PLATFORMS:
                if Context.get_selected_action() not in [Action.COPY, Action.DELETE, Action.EDIT]:
                    self.label_software.pack(
                        side=tk.LEFT,
                        padx=Constants.UI_PAD_SMALL
                    )
                    self.combo_software.pack(
                        side=tk.LEFT,
                        padx=Constants.UI_PAD_SMALL
                    )
                if Context.get_selected_action() not in [Action.COPY, Action.DELETE, Action.EDIT]:
                    self.combo_software.current(0)
                    self.combo_software.event_generate("<<ComboboxSelected>>")
                else:
                    # Initialize UI
                    self.__update_data()
            elif Context.get_selected_category() == Category.CONFIGS:
                if Context.get_selected_action() not in [Action.DELETE, Action.EDIT]:
                    self.label_software.pack(
                        side=tk.LEFT,
                        padx=Constants.UI_PAD_SMALL
                    )
                    self.combo_software.pack(
                        side=tk.LEFT,
                        padx=Constants.UI_PAD_SMALL
                    )
                    self.combo_software.current(0)
                    self.combo_software.event_generate("<<ComboboxSelected>>")
                else:
                    # Initialize UI
                    self.__update_data()
            else:
                # Initialize UI
                self.__update_data()

        # If source is software
        elif event.widget == self.combo_software:
            # Update context from selection
            Context.set_selected_software(None)
            for software in SoftwareId:
                if software.value == self.combo_software.get():
                    Context.set_selected_software(software)

            # Update platforms
            values = []
            for platform in AbstractSoftware.get_registered_software(
                software_id=Context.get_selected_software()
            ).list_platforms():
                values.append(platform)
            values.sort()
            self.combo_platform.configure(
                values=values
            )

            # Select first platform
            if len(values) > 0:
                self.combo_platform.current(0)
                self.combo_platform.event_generate("<<ComboboxSelected>>")
            else:
                self.combo_platform.set('')
                self.combo_platform.event_generate("<<ComboboxSelected>>")

        # If source is platform
        elif event.widget == self.combo_platform:
            # Update context from selection
            Context.set_selected_platform(self.combo_platform.get())

            # Initialize UI
            self.__update_data()

    def __update_data(self):
        """Update data"""

        # Force refresh if no cache exists with data
        if Context.get_setup_file_path().exists() and \
                not Context.get_selected_rows_cache_path().exists():
            # Auto refresh
            self.__load_refresh()
        else:
            # Update UI
            self.__update_ui()

    def __update_ui(self):
        """Update UI with specified rows"""

        # Create table top from Cache
        table_top_rows = XmlHelper.load_xml(
            xml_file_path=Context.get_selected_rows_cache_path()
        )

        self.__create_table_top(
            rows=table_top_rows
        )

        # Create table bottom depending on selected category and action
        components = []
        match(Context.get_selected_category()):
            case Category.GAMES | Category.PLATFORMS:
                if Context.get_selected_action() not in [
                    Action.INSTALL,
                    Action.UNINSTALL,
                    Action.COPY,
                    Action.DELETE,
                    Action.VIEW,
                    Action.EDIT
                ]:
                    if Context.get_selected_software() != SoftwareId.EMU_MOVIES:
                        components.append(Component.INFO)
                if Context.get_selected_action() not in [
                    Action.VIEW,
                    Action.EDIT
                ]:
                    components.append(Component.ROM)
                components.append(Component.MEDIA)

            case Category.CONFIGS:
                components.append(Component.FILES)
                components.append(Component.REGISTRY)

        table_bottom_rows = []
        for component in components:
            table_bottom_rows.append({
                Constants.UI_TABLE_KEY_COL_SELECTION: False,
                Constants.UI_TABLE_KEY_COL_ID: Context.get_text(component.value),
                Constants.UI_TABLE_KEY_COL_NAME: Context.get_text(component.value),
                Constants.UI_TABLE_KEY_COLOR: Constants.ITEM_COLOR_BLACK
            })

        self.__create_table_bottom(
            rows=table_bottom_rows
        )

    def __load_refresh(self, only_ids=None):
        """Load refresh"""

        # Load dialog to refresh
        RefreshDialog(
            self.__window,
            only_ids=only_ids,
            callback=self.__update_ui
        )

    def __load_setup(self):
        """Load setup"""

        # Load dialog to setup
        SetupDialog(
            self.__window,
            callback=self.__update_components_from_context
        )

    def __load_about(self):
        """Load about"""

        # Load dialog for about
        AboutDialog(
            self.__window
        )

    def __execute(self):
        """Execute"""

        # Update selected rows in context
        Context.set_selected_rows(
            self.table_top.get_selected_rows()
        )

        # Update selected components in context
        Context.set_selected_components(
            self.table_bottom.get_selected_rows()
        )

        if Context.get_selected_action() == Action.COPY:
            # If action is COPY, ask to select a folder
            folder_path = filedialog.askdirectory(
                parent=self.__window
            )

            # Cancel execution if no folder selected
            if not folder_path:
                return

            # Update selected folder's path
            Context.set_selected_folder_path(
                folder_path=folder_path
            )

        # Execute
        if Context.get_selected_action() == Action.EDIT:
            selected_component = Context.get_selected_components()[0]
            match(selected_component):

                case Component.MEDIA:
                    # If component MEDIA
                    MediaEditorDialog(
                        self.__window
                    )

                case Component.FILES:
                    # If component FILES
                    ConfigsFilesEditorDialog(
                        self.__window,
                        callback=self.__load_refresh
                    )

                case Component.REGISTRY:
                    # If component REGISTRY
                    ConfigsRegistryEditorDialog(
                        self.__window,
                        callback=self.__load_refresh
                    )
        elif Context.get_selected_action() == Action.VIEW:
            selected_component = Context.get_selected_components()[0]
            match(selected_component):
                case Component.MEDIA:
                    # If component MEDIA
                    MediaEditorDialog(
                        self.__window
                    )
        else:
            ExecuteDialog(
                self.__window,
                callback=self.__load_refresh
            )

    def __create_top_components(self):
        """Create top components"""

        # Create top frame
        top_frame = tk.Frame(self.__window)
        top_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            pady=Constants.UI_PAD_BIG
        )

        # Create criteria frame
        criteria_frame = tk.Frame(top_frame)
        criteria_frame.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )

        # Create Combobox for category
        self.label_category = tk.Label(
            criteria_frame
        )
        self.label_category.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_category = ttk.Combobox(
            criteria_frame,
            width=15
        )
        self.combo_category.config(state="readonly")
        self.combo_category.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_category.bind(
            "<<ComboboxSelected>>",
            self.__on_combo_changed
        )

        # Create Combobox for action
        self.label_action = tk.Label(
            criteria_frame
        )
        self.label_action.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_action = ttk.Combobox(
            criteria_frame,
            width=40
        )
        self.combo_action.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_action.config(state="readonly")
        self.combo_action.bind(
            "<<ComboboxSelected>>",
            self.__on_combo_changed
        )

        # Create Combobox for software
        self.label_software = tk.Label(
            criteria_frame
        )
        self.label_software.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_software = ttk.Combobox(
            criteria_frame,
            width=15
        )
        self.combo_software.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_software.config(state="readonly")
        self.combo_software.bind(
            "<<ComboboxSelected>>",
            self.__on_combo_changed
        )

        # Create Combobox for platform
        self.label_platform = tk.Label(
            criteria_frame
        )
        self.label_platform.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_platform = ttk.Combobox(
            criteria_frame,
            width=40
        )
        self.combo_platform.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_platform.config(state="readonly")
        self.combo_platform.bind(
            "<<ComboboxSelected>>",
            self.__on_combo_changed
        )

        # Create setup/about frame
        setup_about_frame = tk.Frame(top_frame)
        setup_about_frame.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_BIG
        )

        # Button to setup
        self.button_setup = tk.Button(
            setup_about_frame,
            command=self.__load_setup
        )
        self.button_setup.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

        # Button for about
        self.button_about = tk.Button(
            setup_about_frame,
            command=self.__load_about
        )
        self.button_about.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_SMALL
        )

    def __create_center_components(self):
        """Create center components"""
        self.center_frame = tk.Frame(self.__window)
        self.center_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
        )

        self.__create_table_top_frame()
        self.__create_table_bottom_frame()

    def __create_table_top(
        self,
        rows: list
    ):
        """Create the table top"""

        # Clear the frame
        UIHelper.clear_frame(self.table_top_frame)

        # Create the table
        self.table_top = UITable(
            parent=self.table_top_frame,
            on_selected_rows_change=self.__on_selected_rows_changed,
            rows=rows,
            actions_buttons_factory=self.__create_refresh_selection_action_button
        )

    def __create_refresh_selection_action_button(self, master: tk.Misc) -> list[tk.Button]:
        """Create action button for refresh selection"""

        self.refresh_selection_button = tk.Button(
            master,
            text=Context.get_text('refresh_selection'),
            state=tk.DISABLED,
            command=lambda: self.__load_refresh(
                only_ids=self.selected_ids
            )
        )

        self.refresh_all_button = tk.Button(
            master,
            text=Context.get_text('refresh_all'),
            command=self.__load_refresh
        )

        return [
            self.refresh_selection_button,
            self.refresh_all_button
        ]

    def __create_table_bottom(
        self,
        rows: list
    ):
        """Create the table bottom"""

        # Clear the frame
        UIHelper.clear_frame(self.table_bottom_frame)

        # Define if multiple selection
        multiple_selection = True
        if Context.get_selected_action() == Action.EDIT:
            multiple_selection = False

        # Create the table
        self.table_bottom = UITable(
            parent=self.table_bottom_frame,
            on_selected_rows_change=self.__on_selected_rows_changed,
            rows=rows,
            columns_ids=[
                Constants.UI_TABLE_KEY_COL_SELECTION,
                Constants.UI_TABLE_KEY_COL_NAME
            ],
            multiple_selection=multiple_selection
        )

    def __create_table_top_frame(self):
        """Create frame for table"""

        # Create frame
        self.table_top_frame = tk.LabelFrame(
            self.center_frame,
            text=''
        )
        self.table_top_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=Constants.UI_PAD_BIG
        )

    def __create_table_bottom_frame(self):
        """Create frame for table bottom"""

        # Create frame
        self.table_bottom_frame = tk.LabelFrame(
            self.center_frame,
            text=''
        )
        self.table_bottom_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_BIG
        )

    def __create_bottom_components(self):
        """Create bottom components"""

        # Create bottom frame
        bottom_frame = tk.Frame(self.__window)
        bottom_frame.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            pady=Constants.UI_PAD_BIG
        )

        # Create button to execute
        self.button_execute = tk.Button(
            bottom_frame,
            command=self.__execute
        )
        self.button_execute.config(state=tk.DISABLED)
        self.button_execute.pack(
            side=tk.BOTTOM
        )

    def __update_components_from_context(self):
        """Update components from context"""

        # Update context from setup
        Context.set_setup(
            setup=XmlHelper.load_xml(
                xml_file_path=Context.get_setup_file_path()
            )
        )

        # Fix windows's title
        title = Context.get_text('title')
        title += f' ({Context.get_app_version()})'
        if Context.is_simulated():
            title += f' {Context.get_text("simulated")}'
        self.__window.title(title)

        # Fix frames text
        self.table_bottom_frame.config(
            text=Context.get_text('components')
        )

        # Fix buttons text
        self.button_setup.config(
            text=Context.get_text('setup')
        )
        self.button_about.config(
            text=Context.get_text('about')
        )
        self.button_execute.config(
            text=Context.get_text('execute')
        )

        # Fix labels text
        self.label_category.config(
            text=Context.get_text('category')
        )
        self.label_action.config(
            text=Context.get_text('action')
        )
        self.label_software.config(
            text=Context.get_text('software')
        )
        self.label_platform.config(
            text=Context.get_text('platform')
        )

        # Fix values for combobox category
        self.combo_category.config(
            values=[Context.get_text(category.value) for category in Category]
        )

        # Fix values for combobox softwares
        available_softwares = []
        for software in SoftwareId:
            if software in Context.list_available_softwares():
                available_softwares.append(software.value)
        available_softwares.sort()
        self.combo_software.configure(
            values=available_softwares
        )

        # Set default selection
        self.combo_category.set('')
        self.combo_action.set('')
        self.combo_software.set('')
        self.combo_platform.set('')
        self.combo_category.current(0)
        self.combo_category.event_generate("<<ComboboxSelected>>")

        # Fix windows's size and position
        UIHelper.center_window(
            window=self.__window,
            width=1300,
            height=900
        )

    def show(self):
        """Show UI"""

        # Create window
        self.__window = tk.Tk()

        # Handle window close event
        self.__window.protocol("WM_DELETE_WINDOW", self.__on_close)

        # Fix windows's icon
        self.__icon_image = tk.PhotoImage(
            file=os.path.join(
                Context.get_base_path(),
                Constants.PATH_RESOURCES,
                'img',
                'retrobox_manager.png'
            )
        )
        self.__window.iconphoto(
            True,
            self.__icon_image
        )

        # Create components
        self.__create_top_components()
        self.__create_center_components()
        self.__create_bottom_components()

        # If no setup, load setup
        if not Context.get_setup_file_path().exists():
            self.__load_setup()
        else:
            # Update texts
            self.__update_components_from_context()

        # Bind when focus in
        self.__window.bind("<FocusIn>", self.__on_focus_in)

        # Show window
        self.__window.mainloop()

    def __on_close(self):
        """Called when the window is closing"""
        Context.destroy()
        self.__window.destroy()

    def __on_focus_in(self, _):
        """Called when the window if focus in"""

        # Close the window if no available softwares
        if len(Context.list_available_softwares()) == 0:
            self.__on_close()


if __name__ == "__main__":
    # python3 retrobox-manager.py
    app = ApplicationWindow()
    app.show()
