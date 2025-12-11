#!/usr/bin/python3
"""Dialog to setup the application"""

import configparser
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from libraries.constants.constants import Constants, Software
from libraries.context.context import Context
from libraries.ui.ui_helper import UIHelper

# pylint: disable=attribute-defined-outside-init, too-many-locals
# pylint: disable=too-many-instance-attributes, too-many-statements
# pylint: disable=too-many-lines, too-many-branches


class SetupDialog:
    """Dialog to setup the application"""

    def __init__(
        self,
        parent,
        callback: any
    ):
        """Initialize dialog"""

        self.__callback = callback
        self.__loaded = False
        self.__lang_code = Context.get_lang_code()

        # Create dialog
        self.dialog = tk.Toplevel(parent)

        # Fix dialog's size and position
        UIHelper.center_dialog(
            dialog=self.dialog,
            width=800,
            height=400
        )

        # Create top frame
        self.top_frame = tk.Frame(
            self.dialog
        )
        self.top_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_BIG
        )

        # Create center frame
        self.center_frame = tk.Frame(
            self.dialog
        )
        self.center_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_BIG
        )

        # Create bottom frame
        self.bottom_frame = tk.Frame(
            self.dialog
        )
        self.bottom_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=Constants.UI_PAD_SMALL
        )

        # Create components
        self.__create_general_components()
        self.__create_softwares_components()
        self.__create_buttons_components()

        # Update texts in UI Components
        self.__update_ui_components_texts()

        self.__loaded = True

        # Update screen about entry changed
        self.__on_entry_changed(None)

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

    def __validate(self):
        """Validate"""

        # Retrieve general setup
        simulated = self.simulation_boolean_var.get()
        monitor = int(self.combo_monitor.get()) - 1

        # Retrieve softwares setup
        available_softwares = []
        if self.software_batocera_boolean_var.get():
            available_softwares.append(Software.BATOCERA.value)
        if self.software_launchbox_boolean_var.get():
            available_softwares.append(Software.LAUNCHBOX.value)
        if self.software_emu_movies_boolean_var.get():
            available_softwares.append(Software.EMU_MOVIES.value)
        if self.software_skraper_boolean_var.get():
            available_softwares.append(Software.SKRAPER.value)

        # Save setup in a cfg file
        setup = configparser.ConfigParser()
        setup['DEFAULT'] = {
            Constants.SETUP_LANG_CODE: self.__lang_code,
            Constants.SETUP_MONITOR: monitor,
            Constants.SETUP_SIMULATED: simulated,
            Constants.SETUP_AVAILABLE_SOFTWARES: available_softwares
        }

        if self.software_batocera_boolean_var.get():
            setup['DEFAULT'][Constants.SETUP_SOFTWARE_BATOCERA_PATH] = \
                self.entry_software_batocera_path.get()

        if self.software_launchbox_boolean_var.get():
            setup['DEFAULT'][Constants.SETUP_SOFTWARE_LAUNCHBOX_PATH] = \
                self.entry_software_launchbox_path.get()

        if self.software_emu_movies_boolean_var.get():
            setup['DEFAULT'][Constants.SETUP_SOFTWARE_EMU_MOVIES_PATH] = \
                self.entry_software_emu_movies_path.get()

        if self.software_skraper_boolean_var.get():
            setup['DEFAULT'][Constants.SETUP_SOFTWARE_SKRAPER_PATH] = \
                self.entry_software_skraper_path.get()

        setup_file_path = Context.get_setup_file_path()
        setup_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(
            setup_file_path,
            mode='w',
            encoding='UTF-8'
        ) as file:
            setup.write(file)

        # Update context from setup
        Context.update_context_from_setup()

        # Close the dialog after validation
        UIHelper.close_dialog(self.dialog)

        # Call back
        self.__callback()

    def __cancel(self):
        """Cancel"""

        # Close the dialog without saving
        UIHelper.close_dialog(self.dialog)

    def __on_entry_changed(self, *args):
        """Called when an entry changed"""

        if not self.__loaded:
            return

        # Reload UI Texts if the source is the combo lang
        try:
            widget = args[0].widget
            if widget == self.combo_lang:
                self.__lang_code = 'en'
                if self.combo_lang.get() == Context.get_text('lang_fr'):
                    self.__lang_code = 'fr'

                # Update texts in UI Components
                self.__update_ui_components_texts()
        except Exception:
            pass

        # Show/Hide components for software BATOCERA's Path
        if self.software_batocera_boolean_var.get():
            self.software_batocera_path_frame.pack(
                side=tk.RIGHT,
                padx=Constants.UI_PAD_SMALL
            )
        else:
            self.software_batocera_path_frame.pack_forget()
            self.entry_software_batocera_path_var.set('')

        # Show/Hide components for software LAUNCHBOX's Path
        if self.software_launchbox_boolean_var.get():
            self.software_launchbox_path_frame.pack(
                side=tk.RIGHT,
                padx=Constants.UI_PAD_SMALL
            )
        else:
            self.software_launchbox_path_frame.pack_forget()
            self.entry_software_launchbox_path_var.set('')

        # Show/Hide components for software EMU_MOVIES's Path
        if self.software_emu_movies_boolean_var.get():
            self.software_emu_movies_path_frame.pack(
                side=tk.RIGHT,
                padx=Constants.UI_PAD_SMALL
            )
        else:
            self.software_emu_movies_path_frame.pack_forget()
            self.entry_software_emu_movies_path_var.set('')

        # Show/Hide components for software SKRAPER's Path
        if self.software_skraper_boolean_var.get():
            self.software_skraper_path_frame.pack(
                side=tk.RIGHT,
                padx=Constants.UI_PAD_SMALL
            )
        else:
            self.software_skraper_path_frame.pack_forget()
            self.entry_software_skraper_path_var.set('')

        # Enable/Disable button to validate
        validate_enabled = True

        if not self.software_batocera_boolean_var.get() and \
                not self.software_launchbox_boolean_var.get() and \
                not self.software_emu_movies_boolean_var.get() and \
                not self.software_skraper_boolean_var.get():
            validate_enabled = False

        if self.software_batocera_boolean_var.get():
            if len(self.entry_software_batocera_path_var.get()) == 0 or \
                    not Path(self.entry_software_batocera_path_var.get()).exists():
                validate_enabled = False

        if self.software_launchbox_boolean_var.get():
            if len(self.entry_software_launchbox_path_var.get()) == 0 or \
                    not Path(self.entry_software_launchbox_path_var.get()).exists():
                validate_enabled = False

        if self.software_emu_movies_boolean_var.get():
            if len(self.entry_software_emu_movies_path_var.get()) == 0 or \
                    not Path(self.entry_software_emu_movies_path_var.get()).exists():
                validate_enabled = False

        if self.software_skraper_boolean_var.get():
            if len(self.entry_software_skraper_path_var.get()) == 0 or \
                    not Path(self.entry_software_skraper_path_var.get()).exists():
                validate_enabled = False

        if validate_enabled:
            self.button_validate.config(state=tk.NORMAL)
        else:
            self.button_validate.config(state=tk.DISABLED)

    def __create_general_components(self):
        """Create general components"""

        # Create frame
        self.general_frame = tk.LabelFrame(
            self.top_frame
        )
        self.general_frame.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=Constants.UI_PAD_SMALL
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

    def __create_softwares_components(self):
        """Create softwares components"""

        # Create frame
        self.softwares_frame = tk.LabelFrame(
            self.center_frame
        )
        self.softwares_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=Constants.UI_PAD_SMALL
        )

        # Create frame for software BATOCERA
        current_software = Software.BATOCERA
        software_batocera_frame = tk.Frame(self.softwares_frame)
        software_batocera_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.software_batocera_boolean_var = tk.BooleanVar()
        self.software_batocera_boolean_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.software_batocera_boolean_var.set(
            current_software in Context.list_available_softwares()
        )
        software_batocera_checkbox = tk.Checkbutton(
            software_batocera_frame,
            variable=self.software_batocera_boolean_var
        )
        software_batocera_checkbox.pack(
            side=tk.LEFT
        )
        software_batocera_label = tk.Label(
            software_batocera_frame,
            text=current_software.value
        )
        software_batocera_label.pack(
            side=tk.LEFT
        )
        software_batocera_label.bind(
            "<Button-1>",
            lambda e: software_batocera_checkbox.invoke()
        )
        self.software_batocera_path_frame = tk.Frame(
            software_batocera_frame
        )
        self.software_batocera_path_frame.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_SMALL
        )
        self.label_software_batocera_path = tk.Label(
            self.software_batocera_path_frame,
        )
        self.label_software_batocera_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.entry_software_batocera_path_var = tk.StringVar()
        self.entry_software_batocera_path_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.entry_software_batocera_path = tk.Entry(
            self.software_batocera_path_frame,
            textvariable=self.entry_software_batocera_path_var,
            width=40
        )
        self.entry_software_batocera_path.insert(
            0,
            Context.get_software_path(current_software)
        )
        self.entry_software_batocera_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.button_browse_software_batocera_path = tk.Button(
            self.software_batocera_path_frame,
            command=lambda: self.__browse_folder(
                self.entry_software_batocera_path)
        )
        self.button_browse_software_batocera_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

        # Create frame for software LAUNCHBOX
        current_software = Software.LAUNCHBOX
        software_launchbox_frame = tk.Frame(self.softwares_frame)
        software_launchbox_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.software_launchbox_boolean_var = tk.BooleanVar()
        self.software_launchbox_boolean_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.software_launchbox_boolean_var.set(
            current_software in Context.list_available_softwares()
        )
        software_launchbox_checkbox = tk.Checkbutton(
            software_launchbox_frame,
            variable=self.software_launchbox_boolean_var
        )
        software_launchbox_checkbox.pack(
            side=tk.LEFT
        )
        software_launchbox_label = tk.Label(
            software_launchbox_frame,
            text=current_software.value
        )
        software_launchbox_label.pack(
            side=tk.LEFT
        )
        software_launchbox_label.bind(
            "<Button-1>",
            lambda e: software_launchbox_checkbox.invoke()
        )
        self.software_launchbox_path_frame = tk.Frame(
            software_launchbox_frame
        )
        self.software_launchbox_path_frame.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_SMALL
        )
        self.label_software_launchbox_path = tk.Label(
            self.software_launchbox_path_frame
        )
        self.label_software_launchbox_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.entry_software_launchbox_path_var = tk.StringVar()
        self.entry_software_launchbox_path_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.entry_software_launchbox_path = tk.Entry(
            self.software_launchbox_path_frame,
            textvariable=self.entry_software_launchbox_path_var,
            width=40
        )
        self.entry_software_launchbox_path.insert(
            0,
            Context.get_software_path(current_software)
        )
        self.entry_software_launchbox_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.button_browse_software_launchbox_path = tk.Button(
            self.software_launchbox_path_frame,
            command=lambda: self.__browse_folder(
                self.entry_software_launchbox_path)
        )
        self.button_browse_software_launchbox_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

        # Create frame for software EMU_MOVIES
        current_software = Software.EMU_MOVIES
        software_emu_movies_frame = tk.Frame(self.softwares_frame)
        software_emu_movies_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.software_emu_movies_boolean_var = tk.BooleanVar()
        self.software_emu_movies_boolean_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.software_emu_movies_boolean_var.set(
            current_software in Context.list_available_softwares()
        )
        software_emu_movies_checkbox = tk.Checkbutton(
            software_emu_movies_frame,
            variable=self.software_emu_movies_boolean_var
        )
        software_emu_movies_checkbox.pack(
            side=tk.LEFT
        )
        software_emu_movies_label = tk.Label(
            software_emu_movies_frame,
            text=current_software.value
        )
        software_emu_movies_label.pack(
            side=tk.LEFT
        )
        software_emu_movies_label.bind(
            "<Button-1>",
            lambda e: software_emu_movies_checkbox.invoke()
        )
        self.software_emu_movies_path_frame = tk.Frame(
            software_emu_movies_frame
        )
        self.software_emu_movies_path_frame.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_SMALL
        )
        self.label_software_emu_movies_path = tk.Label(
            self.software_emu_movies_path_frame,
        )
        self.label_software_emu_movies_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.entry_software_emu_movies_path_var = tk.StringVar()
        self.entry_software_emu_movies_path_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.entry_software_emu_movies_path = tk.Entry(
            self.software_emu_movies_path_frame,
            textvariable=self.entry_software_emu_movies_path_var,
            width=40
        )
        self.entry_software_emu_movies_path.insert(
            0,
            Context.get_software_path(current_software)
        )
        self.entry_software_emu_movies_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.button_browse_software_emu_movies_path = tk.Button(
            self.software_emu_movies_path_frame,
            command=lambda: self.__browse_folder(
                self.entry_software_emu_movies_path)
        )
        self.button_browse_software_emu_movies_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

        # Create frame for software SKRAPER
        current_software = Software.SKRAPER
        software_skraper_frame = tk.Frame(self.softwares_frame)
        software_skraper_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.software_skraper_boolean_var = tk.BooleanVar()
        self.software_skraper_boolean_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.software_skraper_boolean_var.set(
            current_software in Context.list_available_softwares()
        )
        software_skraper_checkbox = tk.Checkbutton(
            software_skraper_frame,
            variable=self.software_skraper_boolean_var
        )
        software_skraper_checkbox.pack(
            side=tk.LEFT
        )
        software_skraper_label = tk.Label(
            software_skraper_frame,
            text=current_software.value
        )
        software_skraper_label.pack(
            side=tk.LEFT
        )
        software_skraper_label.bind(
            "<Button-1>",
            lambda e: software_skraper_checkbox.invoke()
        )
        self.software_skraper_path_frame = tk.Frame(
            software_skraper_frame
        )
        self.software_skraper_path_frame.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_SMALL
        )
        self.label_software_skraper_path = tk.Label(
            self.software_skraper_path_frame
        )
        self.label_software_skraper_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.entry_software_skraper_path_var = tk.StringVar()
        self.entry_software_skraper_path_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.entry_software_skraper_path = tk.Entry(
            self.software_skraper_path_frame,
            textvariable=self.entry_software_skraper_path_var,
            width=40
        )
        self.entry_software_skraper_path.insert(
            0,
            Context.get_software_path(current_software)
        )
        self.entry_software_skraper_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.button_browse_software_skraper_path = tk.Button(
            self.software_skraper_path_frame,
            command=lambda: self.__browse_folder(
                self.entry_software_skraper_path)
        )
        self.button_browse_software_skraper_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

    def __create_buttons_components(self):
        """Create bottom components"""

        # Create buttons frame
        buttons_frame = tk.Frame(self.dialog)
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
            command=self.__validate
        )
        self.button_validate.config(state=tk.DISABLED)
        self.button_validate.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

    def __update_ui_components_texts(self):
        """Update texts in UI Components"""

        self.dialog.title(Context.get_text(
            'setup',
            lang=self.__lang_code
        ))

        self.label_lang.config(
            text=Context.get_text(
                'lang',
                lang=self.__lang_code
            )
        )

        self.combo_lang.config(
            values=[
                Context.get_text(
                    'lang_fr',
                    lang=self.__lang_code
                ),
                Context.get_text(
                    'lang_en',
                    lang=self.__lang_code
                )
            ]
        )
        self.combo_lang.set(
            Context.get_text(
                f'lang_{self.__lang_code}',
                lang=self.__lang_code
            )
        )

        self.general_frame.config(
            text=Context.get_text(
                'setup_general',
                lang=self.__lang_code
            )
        )

        self.label_monitor.config(
            text=Context.get_text(
                'monitor',
                lang=self.__lang_code
            )
        )

        self.label_simulation.config(
            text=Context.get_text(
                'simulation',
                lang=self.__lang_code
            )
        )

        self.softwares_frame.config(
            text=Context.get_text(
                'setup_softwares',
                lang=self.__lang_code
            )
        )

        self.button_browse_software_batocera_path.config(
            text=Context.get_text(
                'browse',
                lang=self.__lang_code
            )
        )

        self.button_browse_software_launchbox_path.config(
            text=Context.get_text(
                'browse',
                lang=self.__lang_code
            )
        )

        self.softwares_frame.config(
            text=Context.get_text(
                'setup_softwares',
                lang=self.__lang_code
            )
        )

        self.button_browse_software_emu_movies_path.config(
            text=Context.get_text(
                'browse',
                lang=self.__lang_code
            )
        )

        self.button_browse_software_skraper_path.config(
            text=Context.get_text(
                'browse',
                lang=self.__lang_code
            )
        )

        self.button_cancel.config(
            text=Context.get_text(
                'cancel',
                lang=self.__lang_code
            )
        )

        self.button_validate.config(
            text=Context.get_text(
                'validate',
                lang=self.__lang_code
            )
        )
