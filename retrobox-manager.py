
# pylint: disable=invalid-name
#!/usr/bin/python3
"""Application to manage my Retrobox"""

import os
import tkinter as tk
from tkinter import ttk

from dialogs.about.about_dialog import AboutDialog
from dialogs.setup.setup_dialog import SetupDialog
from libraries.constants.constants import Action, Constants, FrontEnd
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.ui.ui_helper import UIHelper
from libraries.xml.xml_helper import XmlHelper

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

        # If source is action
        if event.widget == self.combo_action:
            # Update context from selection
            Context.set_selected_action(
                list(Action)[self.combo_action.current()]
            )

            # Select first front end
            self.combo_front_end.current(0)
            self.combo_front_end.event_generate("<<ComboboxSelected>>")

        # If source is front end
        if event.widget == self.combo_front_end:
            # Update context from selection
            Context.set_selected_front_end(
                list(FrontEnd)[self.combo_front_end.current()]
            )

            # Update platforms
            platforms = []
            if Context.get_selected_action() == Action.EXPORT:
                if Context.get_selected_front_end() == FrontEnd.BATOCERA:
                    for platform in FileHelper.list_sub_directories(
                        folder_path=os.path.join(
                            Context.get_front_end_path(
                                front_end=Context.get_selected_front_end()
                            ),
                            Constants.BATOCERA_ROMS_PATH
                        )
                    ):
                        if not FileHelper.is_file_exists(os.path.join(
                            Context.get_front_end_path(
                                front_end=Context.get_selected_front_end()
                            ),
                            Constants.BATOCERA_ROMS_PATH,
                            platform,
                            Constants.BATOCERA_GAMELIST_PATH
                        )):
                            continue

                        platforms.append(platform)
                elif Context.get_selected_front_end() == FrontEnd.LAUNCHBOX:
                    for relative_path in FileHelper.list_relative_paths(
                        folder_path=os.path.join(
                            Context.get_front_end_path(
                                front_end=Context.get_selected_front_end()
                            ),
                            Constants.LAUNCHBOX_DATA_PATH,
                            Constants.LAUNCHBOX_PLATFORMS_PATH
                        ),
                        file_name='*',
                        error_if_not_found=False
                    ):
                        if not relative_path.endswith(Constants.XML_EXTENSION):
                            continue
                        platforms.append(
                            relative_path[:-len(Constants.XML_EXTENSION)]
                        )
            else:
                platforms = FileHelper.list_sub_directories(
                    folder_path=Context.get_games_path()
                )
            self.combo_platform.configure(
                values=platforms
            )

            # Select first front platform
            if len(platforms) > 0:
                self.combo_platform.current(0)
                self.combo_platform.event_generate("<<ComboboxSelected>>")

        # If source is platform
        elif event.widget == self.combo_platform:
            # Update context from selection
            Context.set_selected_platform(self.combo_platform.get())

            # List games
            if Context.get_selected_action() == Action.EXPORT:
                if Context.get_selected_front_end() == FrontEnd.BATOCERA:
                    gamelist = XmlHelper.list_tag_values(
                        xml_file_path=os.path.join(
                            Context.get_front_end_path(
                                front_end=Context.get_selected_front_end()
                            ),
                            Constants.BATOCERA_ROMS_PATH,
                            Context.get_selected_platform(),
                            Constants.BATOCERA_GAMELIST_PATH
                        ),
                        parent_tag='game',
                        tag='name'
                    )
                    print(gamelist)

                elif Context.get_selected_front_end() == FrontEnd.LAUNCHBOX:
                    gamelist = XmlHelper.list_tag_values(
                        xml_file_path=os.path.join(
                            Context.get_front_end_path(
                                front_end=Context.get_selected_front_end()
                            ),
                            Constants.LAUNCHBOX_DATA_PATH,
                            Constants.LAUNCHBOX_PLATFORMS_PATH,
                            f'{Context.get_selected_platform()}{Constants.XML_EXTENSION}'
                        ),
                        parent_tag='Game',
                        tag='Title'
                    )
                    print(gamelist)

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

        # Create Combobox for front ends
        self.label_front_end = tk.Label(
            combo_frame
        )
        self.label_front_end.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_front_end = ttk.Combobox(
            combo_frame,
            width=20
        )
        self.combo_front_end.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.combo_front_end.config(state="readonly")
        self.combo_front_end.bind(
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
            width=35
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

        # Set front ends
        front_ends = []
        for front_end in FrontEnd:
            front_ends.append(front_end.value)
        self.combo_front_end.configure(
            values=front_ends
        )
        self.combo_front_end.current(0)
        self.combo_front_end.event_generate("<<ComboboxSelected>>")

        # Set actions
        actions = []
        for action in Action:
            actions.append(Context.get_text(
                action.value
            ))
        self.combo_action.configure(
            values=actions
        )
        self.combo_action.current(0)
        self.combo_action.event_generate("<<ComboboxSelected>>")

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
        self.label_front_end.config(
            text=Context.get_text('front_end')
        )
        self.label_platform.config(
            text=Context.get_text('platform')
        )

        # Fix combobox text
        self.combo_action.config(
            values=[Context.get_text(action.value) for action in Action]
        )

        # Set default selection
        self.combo_action.current(0)
        self.combo_action.event_generate("<<ComboboxSelected>>")

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
