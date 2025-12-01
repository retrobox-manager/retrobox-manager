#!/usr/bin/python3
"""Dialog to setup the application"""

import configparser
import tkinter as tk
from tkinter import ttk

from libraries.constants.constants import Constants
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
            height=180
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
        self.__create_buttons_components()

        # Update texts in UI Components
        self.__update_ui_components_texts()

        self.__loaded = True

        # Update screen about entry changed
        self.__on_entry_changed(None)

    def __validate(self):
        """Validate"""

        # Retrieve general setup
        simulated = self.simulation_boolean_var.get()
        monitor = int(self.combo_monitor.get()) - 1

        # Save setup in a cfg file
        setup = configparser.ConfigParser()
        setup['DEFAULT'] = {
            Constants.SETUP_LANG_CODE: self.__lang_code,
            Constants.SETUP_MONITOR: monitor,
            Constants.SETUP_SIMULATED: simulated
        }

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

        # Enable/Disable button to validate
        validate_enabled = True

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
