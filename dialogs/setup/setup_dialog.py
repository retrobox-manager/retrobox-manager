#!/usr/bin/python3
"""Dialog to setup the application"""

import configparser
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from libraries.constants.constants import Constants, FrontEnd, Scraper
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
        self.__create_front_ends_components()
        self.__create_scrapers_components()
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

        # Retrieve front ends setup
        available_front_ends = []
        if self.front_end_batocera_boolean_var.get():
            available_front_ends.append(FrontEnd.BATOCERA.value)
        if self.front_end_launchbox_boolean_var.get():
            available_front_ends.append(FrontEnd.LAUNCHBOX.value)

        # Retrieve scrapers setup
        available_scrapers = []
        if self.scraper_emu_movies_boolean_var.get():
            available_scrapers.append(Scraper.EMU_MOVIES.value)
        if self.scraper_skraper_boolean_var.get():
            available_scrapers.append(Scraper.SKRAPER.value)

        # Save setup in a cfg file
        setup = configparser.ConfigParser()
        setup['DEFAULT'] = {
            Constants.SETUP_LANG_CODE: self.__lang_code,
            Constants.SETUP_MONITOR: monitor,
            Constants.SETUP_SIMULATED: simulated,
            Constants.SETUP_AVAILABLE_FRONT_ENDS: available_front_ends,
            Constants.SETUP_AVAILABLE_SCRAPERS: available_scrapers
        }

        if self.front_end_batocera_boolean_var.get():
            setup['DEFAULT'][Constants.SETUP_FRONT_END_BATOCERA_PATH] = \
                self.entry_front_end_batocera_path.get()

        if self.front_end_launchbox_boolean_var.get():
            setup['DEFAULT'][Constants.SETUP_FRONT_END_LAUNCHBOX_PATH] = \
                self.entry_front_end_launchbox_path.get()

        if self.scraper_emu_movies_boolean_var.get():
            setup['DEFAULT'][Constants.SETUP_SCRAPER_EMU_MOVIES_PATH] = \
                self.entry_scraper_emu_movies_path.get()

        if self.scraper_skraper_boolean_var.get():
            setup['DEFAULT'][Constants.SETUP_SCRAPER_SKRAPER_PATH] = \
                self.entry_scraper_skraper_path.get()

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

        # Show/Hide components for front end BATOCERA's Path
        if self.front_end_batocera_boolean_var.get():
            self.front_end_batocera_path_frame.pack(
                side=tk.RIGHT,
                padx=Constants.UI_PAD_SMALL
            )
        else:
            self.front_end_batocera_path_frame.pack_forget()
            self.entry_front_end_batocera_path_var.set('')

        # Show/Hide components for front end LAUNCHBOX's Path
        if self.front_end_launchbox_boolean_var.get():
            self.front_end_launchbox_path_frame.pack(
                side=tk.RIGHT,
                padx=Constants.UI_PAD_SMALL
            )
        else:
            self.front_end_launchbox_path_frame.pack_forget()
            self.entry_front_end_launchbox_path_var.set('')

        # Show/Hide components for scraper EMU_MOVIES's Path
        if self.scraper_emu_movies_boolean_var.get():
            self.scraper_emu_movies_path_frame.pack(
                side=tk.RIGHT,
                padx=Constants.UI_PAD_SMALL
            )
        else:
            self.scraper_emu_movies_path_frame.pack_forget()
            self.entry_scraper_emu_movies_path_var.set('')

        # Show/Hide components for scraper SKRAPER's Path
        if self.scraper_skraper_boolean_var.get():
            self.scraper_skraper_path_frame.pack(
                side=tk.RIGHT,
                padx=Constants.UI_PAD_SMALL
            )
        else:
            self.scraper_skraper_path_frame.pack_forget()
            self.entry_scraper_skraper_path_var.set('')

        # Enable/Disable button to validate
        validate_enabled = True

        if not self.front_end_batocera_boolean_var.get() and \
                not self.front_end_launchbox_boolean_var.get():
            validate_enabled = False

        if self.front_end_batocera_boolean_var.get():
            if len(self.entry_front_end_batocera_path_var.get()) == 0 or \
                    not Path(self.entry_front_end_batocera_path_var.get()).exists():
                validate_enabled = False

        if self.front_end_launchbox_boolean_var.get():
            if len(self.entry_front_end_launchbox_path_var.get()) == 0 or \
                    not Path(self.entry_front_end_launchbox_path_var.get()).exists():
                validate_enabled = False

        if not self.scraper_emu_movies_boolean_var.get() and \
                not self.scraper_skraper_boolean_var.get():
            validate_enabled = False

        if self.scraper_emu_movies_boolean_var.get():
            if len(self.entry_scraper_emu_movies_path_var.get()) == 0 or \
                    not Path(self.entry_scraper_emu_movies_path_var.get()).exists():
                validate_enabled = False

        if self.scraper_skraper_boolean_var.get():
            if len(self.entry_scraper_skraper_path_var.get()) == 0 or \
                    not Path(self.entry_scraper_skraper_path_var.get()).exists():
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

    def __create_front_ends_components(self):
        """Create front ends components"""

        # Create frame
        self.front_ends_frame = tk.LabelFrame(
            self.center_frame
        )
        self.front_ends_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=Constants.UI_PAD_SMALL
        )

        # Create frame for front end BATOCERA
        current_front_end = FrontEnd.BATOCERA
        front_end_batocera_frame = tk.Frame(self.front_ends_frame)
        front_end_batocera_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.front_end_batocera_boolean_var = tk.BooleanVar()
        self.front_end_batocera_boolean_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.front_end_batocera_boolean_var.set(
            current_front_end.value in Context.list_available_front_ends()
        )
        front_end_batocera_checkbox = tk.Checkbutton(
            front_end_batocera_frame,
            variable=self.front_end_batocera_boolean_var
        )
        front_end_batocera_checkbox.pack(
            side=tk.LEFT
        )
        front_end_batocera_label = tk.Label(
            front_end_batocera_frame,
            text=current_front_end.value
        )
        front_end_batocera_label.pack(
            side=tk.LEFT
        )
        front_end_batocera_label.bind(
            "<Button-1>",
            lambda e: front_end_batocera_checkbox.invoke()
        )
        self.front_end_batocera_path_frame = tk.Frame(
            front_end_batocera_frame
        )
        self.front_end_batocera_path_frame.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_SMALL
        )
        self.label_front_end_batocera_path = tk.Label(
            self.front_end_batocera_path_frame,
        )
        self.label_front_end_batocera_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.entry_front_end_batocera_path_var = tk.StringVar()
        self.entry_front_end_batocera_path_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.entry_front_end_batocera_path = tk.Entry(
            self.front_end_batocera_path_frame,
            textvariable=self.entry_front_end_batocera_path_var,
            width=40
        )
        self.entry_front_end_batocera_path.insert(
            0,
            Context.get_front_end_path(current_front_end)
        )
        self.entry_front_end_batocera_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.button_browse_front_end_batocera_path = tk.Button(
            self.front_end_batocera_path_frame,
            command=lambda: self.__browse_folder(
                self.entry_front_end_batocera_path)
        )
        self.button_browse_front_end_batocera_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

        # Create frame for front end LAUNCHBOX
        current_front_end = FrontEnd.LAUNCHBOX
        front_end_launchbox_frame = tk.Frame(self.front_ends_frame)
        front_end_launchbox_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.front_end_launchbox_boolean_var = tk.BooleanVar()
        self.front_end_launchbox_boolean_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.front_end_launchbox_boolean_var.set(
            current_front_end.value in Context.list_available_front_ends()
        )
        front_end_launchbox_checkbox = tk.Checkbutton(
            front_end_launchbox_frame,
            variable=self.front_end_launchbox_boolean_var
        )
        front_end_launchbox_checkbox.pack(
            side=tk.LEFT
        )
        front_end_launchbox_label = tk.Label(
            front_end_launchbox_frame,
            text=current_front_end.value
        )
        front_end_launchbox_label.pack(
            side=tk.LEFT
        )
        front_end_launchbox_label.bind(
            "<Button-1>",
            lambda e: front_end_launchbox_checkbox.invoke()
        )
        self.front_end_launchbox_path_frame = tk.Frame(
            front_end_launchbox_frame
        )
        self.front_end_launchbox_path_frame.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_SMALL
        )
        self.label_front_end_launchbox_path = tk.Label(
            self.front_end_launchbox_path_frame
        )
        self.label_front_end_launchbox_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.entry_front_end_launchbox_path_var = tk.StringVar()
        self.entry_front_end_launchbox_path_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.entry_front_end_launchbox_path = tk.Entry(
            self.front_end_launchbox_path_frame,
            textvariable=self.entry_front_end_launchbox_path_var,
            width=40
        )
        self.entry_front_end_launchbox_path.insert(
            0,
            Context.get_front_end_path(current_front_end)
        )
        self.entry_front_end_launchbox_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.button_browse_front_end_launchbox_path = tk.Button(
            self.front_end_launchbox_path_frame,
            command=lambda: self.__browse_folder(
                self.entry_front_end_launchbox_path)
        )
        self.button_browse_front_end_launchbox_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

    def __create_scrapers_components(self):
        """Create scrapers components"""

        # Create frame
        self.scrapers_frame = tk.LabelFrame(
            self.center_frame
        )
        self.scrapers_frame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_BIG
        )

        # Create frame for scraper EMU_MOVIES
        current_scraper = Scraper.EMU_MOVIES
        scraper_emu_movies_frame = tk.Frame(self.scrapers_frame)
        scraper_emu_movies_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.scraper_emu_movies_boolean_var = tk.BooleanVar()
        self.scraper_emu_movies_boolean_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.scraper_emu_movies_boolean_var.set(
            current_scraper.value in Context.list_available_scrapers()
        )
        scraper_emu_movies_checkbox = tk.Checkbutton(
            scraper_emu_movies_frame,
            variable=self.scraper_emu_movies_boolean_var
        )
        scraper_emu_movies_checkbox.pack(
            side=tk.LEFT
        )
        scraper_emu_movies_label = tk.Label(
            scraper_emu_movies_frame,
            text=current_scraper.value
        )
        scraper_emu_movies_label.pack(
            side=tk.LEFT
        )
        scraper_emu_movies_label.bind(
            "<Button-1>",
            lambda e: scraper_emu_movies_checkbox.invoke()
        )
        self.scraper_emu_movies_path_frame = tk.Frame(
            scraper_emu_movies_frame
        )
        self.scraper_emu_movies_path_frame.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_SMALL
        )
        self.label_scraper_emu_movies_path = tk.Label(
            self.scraper_emu_movies_path_frame,
        )
        self.label_scraper_emu_movies_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.entry_scraper_emu_movies_path_var = tk.StringVar()
        self.entry_scraper_emu_movies_path_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.entry_scraper_emu_movies_path = tk.Entry(
            self.scraper_emu_movies_path_frame,
            textvariable=self.entry_scraper_emu_movies_path_var,
            width=40
        )
        self.entry_scraper_emu_movies_path.insert(
            0,
            Context.get_scraper_path(current_scraper)
        )
        self.entry_scraper_emu_movies_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.button_browse_scraper_emu_movies_path = tk.Button(
            self.scraper_emu_movies_path_frame,
            command=lambda: self.__browse_folder(
                self.entry_scraper_emu_movies_path)
        )
        self.button_browse_scraper_emu_movies_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )

        # Create frame for scraper SKRAPER
        current_scraper = Scraper.SKRAPER
        scraper_skraper_frame = tk.Frame(self.scrapers_frame)
        scraper_skraper_frame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.scraper_skraper_boolean_var = tk.BooleanVar()
        self.scraper_skraper_boolean_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.scraper_skraper_boolean_var.set(
            current_scraper.value in Context.list_available_scrapers()
        )
        scraper_skraper_checkbox = tk.Checkbutton(
            scraper_skraper_frame,
            variable=self.scraper_skraper_boolean_var
        )
        scraper_skraper_checkbox.pack(
            side=tk.LEFT
        )
        scraper_skraper_label = tk.Label(
            scraper_skraper_frame,
            text=current_scraper.value
        )
        scraper_skraper_label.pack(
            side=tk.LEFT
        )
        scraper_skraper_label.bind(
            "<Button-1>",
            lambda e: scraper_skraper_checkbox.invoke()
        )
        self.scraper_skraper_path_frame = tk.Frame(
            scraper_skraper_frame
        )
        self.scraper_skraper_path_frame.pack(
            side=tk.RIGHT,
            padx=Constants.UI_PAD_SMALL
        )
        self.label_scraper_skraper_path = tk.Label(
            self.scraper_skraper_path_frame
        )
        self.label_scraper_skraper_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.entry_scraper_skraper_path_var = tk.StringVar()
        self.entry_scraper_skraper_path_var.trace_add(
            "write",
            self.__on_entry_changed
        )
        self.entry_scraper_skraper_path = tk.Entry(
            self.scraper_skraper_path_frame,
            textvariable=self.entry_scraper_skraper_path_var,
            width=40
        )
        self.entry_scraper_skraper_path.insert(
            0,
            Context.get_scraper_path(current_scraper)
        )
        self.entry_scraper_skraper_path.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL
        )
        self.button_browse_scraper_skraper_path = tk.Button(
            self.scraper_skraper_path_frame,
            command=lambda: self.__browse_folder(
                self.entry_scraper_skraper_path)
        )
        self.button_browse_scraper_skraper_path.pack(
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

        self.front_ends_frame.config(
            text=Context.get_text(
                'setup_front_ends',
                lang=self.__lang_code
            )
        )

        self.button_browse_front_end_batocera_path.config(
            text=Context.get_text(
                'browse',
                lang=self.__lang_code
            )
        )

        self.button_browse_front_end_launchbox_path.config(
            text=Context.get_text(
                'browse',
                lang=self.__lang_code
            )
        )

        self.scrapers_frame.config(
            text=Context.get_text(
                'setup_scrapers',
                lang=self.__lang_code
            )
        )

        self.button_browse_scraper_emu_movies_path.config(
            text=Context.get_text(
                'browse',
                lang=self.__lang_code
            )
        )

        self.button_browse_scraper_skraper_path.config(
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
