
# pylint: disable=invalid-name
#!/usr/bin/python3
"""Application to manage my Retrobox"""

import os
import tkinter as tk
from tkinter import ttk

from dialogs.about.about_dialog import AboutDialog
from dialogs.setup.setup_dialog import SetupDialog
from libraries.constants.constants import Constants
from libraries.context.context import Context
from libraries.ui.ui_helper import UIHelper

# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals
# pylint: disable=too-many-lines


class ApplicationWindow:
    """Application to manage Retrobox"""

    def __on_combo_changed(self, event):
        """Called when a combo changed"""

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
            width=35
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

    def __create_bottom_components(self):
        """Create bottom components"""

        # Create bottom frame
        bottom_frame = tk.Frame(self.__window)
        bottom_frame.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            pady=Constants.UI_PAD_BIG
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

        # Fix labels text
        self.label_action.config(
            text=Context.get_text('action')
        )

        # Set default selection
        self.combo_action.set('')

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
