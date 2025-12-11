# pylint: disable=invalid-name
#!/usr/bin/python3
"""Application to manage my Retrobox"""

import os
import tkinter as tk
from tkinter import ttk

from dialogs.about.about_dialog import AboutDialog
from dialogs.execute.execute_dialog import ExecuteDialog
from dialogs.setup.setup_dialog import SetupDialog
from manager.manager_factory import ManagerFactory
from libraries.constants.constants import Action, Category, Constants, Platform, Software
from libraries.context.context import Context
from libraries.text.text_helper import TextHelper
from libraries.ui.ui_helper import UIHelper
from libraries.ui.ui_table import UITable

# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-instance-attributes


class ApplicationWindow:
    """Application to manage Retrobox"""

    def __on_selected_rows_changed(self):
        """Called when selected rows changed"""

        # Retrieve selected rows
        selected_rows = self.table.get_selected_rows()

        # Update execute button state
        if len(selected_rows) > 0:
            self.button_execute.config(state=tk.NORMAL)
        else:
            self.button_execute.config(state=tk.DISABLED)

    def __on_combo_changed(self, event):
        """Called when a combo changed"""

        # If source is category
        if event.widget == self.combo_category:
            # Update context from selection
            Context.set_selected_category(
                list(Category)[self.combo_category.current()]
            )

            # Set title for table
            self.table_frame.config(
                text=Context.get_text(
                    Context.get_selected_category().value
                )
            )

            # Show/Hide combos depending on selected category
            if Context.get_selected_category() == Category.GAMES:
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
                self.combo_software.current(0)
            else:
                self.label_software.pack_forget()
                self.combo_software.pack_forget()
                self.label_platform.pack_forget()
                self.combo_platform.pack_forget()

            # Update actions depending on selected category
            available_actions = []
            match(Context.get_selected_category()):
                case Category.GAMES:
                    available_actions = [
                        Action.EXPORT,
                        Action.INSTALL,
                        Action.UNINSTALL
                    ]

                case Category.CONFIGS:
                    available_actions = [
                        Action.EDIT,
                        Action.INSTALL,
                        Action.UNINSTALL
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
            Context.set_selected_action(
                list(Action)[self.combo_action.current()]
            )

            # Select first software
            self.combo_software.current(0)
            self.combo_software.event_generate("<<ComboboxSelected>>")

        # If source is software
        elif event.widget == self.combo_software:
            # Update context from selection
            Context.set_selected_software(
                list(Software)[self.combo_software.current()]
            )

            # Update platforms
            values = []
            for platform in ManagerFactory.create(
                software=Context.get_selected_software()
            ).list_platforms():
                values.append(platform.value)
            self.combo_platform.configure(
                values=values
            )

            # Select first software
            if len(values) > 0:
                self.combo_platform.current(0)
                self.combo_platform.event_generate("<<ComboboxSelected>>")
            else:
                self.combo_platform.set('')
                self.combo_platform.event_generate("<<ComboboxSelected>>")

        # If source is platform
        elif event.widget == self.combo_platform:
            # Update context from selection
            Context.set_selected_platform(
                list(Platform)[self.combo_platform.current()]
            )

            # Update UI
            self.__update_ui()

    def __update_ui(self):
        """Update UI depending on choices made in combos"""

        # Create rows for table
        table_rows = []
        match(Context.get_selected_action()):
            case Action.EXPORT:
                games = ManagerFactory.create(
                    software=Context.get_selected_software()
                ).list_games(
                    platform=Context.get_selected_platform()
                )

                for game in games:
                    # Build row
                    row = {}
                    row[Constants.UI_TABLE_KEY_COL_SELECTION] = False
                    row[Constants.UI_TABLE_KEY_COL_ID] = TextHelper.sanitize(
                        game
                    )
                    row[Constants.UI_TABLE_KEY_COL_NAME] = game

                    # Retrieve color
                    row[Constants.UI_TABLE_KEY_COLOR] = Constants.ITEM_COLOR_GREEN

                    # Append row
                    table_rows.append(row)

        # Sort rows depending on UI_TABLE_KEY_COLOR (desc) and Constants.UI_TABLE_KEY_COL_NAME (asc)
        sorted_rows = sorted(
            table_rows,
            key=lambda x: (-ord(
                x[Constants.UI_TABLE_KEY_COLOR][0]),
                x[Constants.UI_TABLE_KEY_COL_NAME]
            )
        )

        self.__create_table(
            rows=sorted_rows
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
            self.table.get_selected_rows()
        )

        # Update context
        ExecuteDialog(
            self.__window,
            callback=self.__update_ui
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

        # Create combo frame
        combo_frame = tk.Frame(top_frame)
        combo_frame.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )

        # Create Combobox for category
        self.label_category = tk.Label(
            combo_frame
        )
        self.label_category.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_category = ttk.Combobox(
            combo_frame,
            width=7
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
            combo_frame
        )
        self.label_action.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_action = ttk.Combobox(
            combo_frame,
            width=25
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

        # Create Combobox for softwares
        self.label_software = tk.Label(
            combo_frame
        )
        self.label_software.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_software = ttk.Combobox(
            combo_frame,
            width=10
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
            combo_frame
        )
        self.label_platform.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_platform = ttk.Combobox(
            combo_frame,
            width=25
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

        self.__create_table_frame()

    def __create_table(
        self,
        rows: list
    ):
        """Create the table"""

        # Clear the frame
        UIHelper.clear_frame(self.table_frame)

        # Create the table
        self.table = UITable(
            parent=self.table_frame,
            on_selected_rows_change=self.__on_selected_rows_changed,
            rows=rows
        )

    def __create_table_frame(self):
        """Create frame for table"""

        # Create frame
        self.table_frame = tk.LabelFrame(
            self.center_frame,
            text=''
        )
        self.table_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=Constants.UI_PAD_BIG
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

        # Fix windows's title
        title = Context.get_text('title')
        title += f' ({Context.get_app_version()})'
        if Context.is_simulated():
            title += f' {Context.get_text("simulated")}'
        self.__window.title(title)

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
        for software in Software:
            if software in Context.list_available_softwares():
                available_softwares.append(software.value)
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
            width=1024,
            height=768
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
                Constants.RESOURCES_PATH,
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

        # Update texts
        self.__update_components_from_context()

        # If no setup, load setup
        if not Context.get_setup_file_path().exists():
            self.__load_setup()

        # Show window
        self.__window.mainloop()

    def __on_close(self):
        """Called when the window is closing"""
        Context.destroy()
        self.__window.destroy()


if __name__ == "__main__":
    # python3 retrobox-manager.py
    app = ApplicationWindow()
    app.show()
