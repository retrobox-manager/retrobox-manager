#!/usr/bin/python3
"""Abstract Executor"""

from abc import ABC, abstractmethod
import threading
import time
import tkinter as tk
from tkinter import ttk

from libraries.constants.constants import Action, Category, Constants
from libraries.context.context import Context
from libraries.logging.logging_helper import LoggingHelper

# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments


class AbstractExecutor(ABC):
    """Abstract Executor (Common for all executors)"""

    def __init__(
        self,
        sub_items_enabled: bool
    ):
        """Initialize executor"""

        self.__execution_finished: bool = False
        self.__stop_execution = threading.Event()
        self.__progress_bar = None
        self.__progress_label = None
        self.__sub_progress_bar = None
        self.__sub_progress_label = None
        self.__button_close = None
        self.__ids_dones = []
        self.__sub_items_enabled = sub_items_enabled

    def is_sub_items_enabled(self) -> bool:
        """Specify if function sub items is enabled"""

        return self.__sub_items_enabled

    def set_ui_components(
        self,
        progress_bar: ttk.Progressbar,
        progress_label: tk.Label,
        sub_progress_bar: ttk.Progressbar,
        sub_progress_label: tk.Label,
        button_close: tk.Button
    ):
        """Set UI Components"""

        self.__progress_bar = progress_bar
        self.__progress_label = progress_label
        self.__sub_progress_bar = sub_progress_bar
        self.__sub_progress_label = sub_progress_label
        self.__button_close = button_close

    def stop_execution(self):
        """Stop execution"""

        self.__stop_execution.set()

    def is_execution_finished(self) -> bool:
        """Specify if execution finished"""

        return self.__execution_finished

    # pylint: disable=unused-argument
    def confirm_execution(self, parent: any) -> True:
        """Confirm for execution"""

        # No confirmation by default
        return True

    def execute(self):
        """Execute"""

        if self.__progress_bar is None or \
            self.__progress_label is None or \
                self.__button_close is None:
            raise Exception('Missing UI components!')

        # Fix text Stop for button to close
        self.__button_close.config(
            text=Context.get_text('stop')
        )

        # Show message for execution started
        LoggingHelper.log_info(
            message=Context.get_text(
                'execution_started',
                action=Context.get_text(
                    Context.get_selected_action().value,
                    category=Context.get_text(
                        Context.get_selected_category().value
                    )
                )
            )
        )

        # Retrieve selected rows
        rows = Context.get_selected_rows()

        # Initialize progress bar
        self.__progress_bar.config(maximum=len(rows))

        item_current_counter = 1
        for row in rows:

            # Stop if execution stopped
            if self.__stop_execution.is_set():
                return

            # Increment progress bar
            self.__progress_bar['value'] = item_current_counter
            self.__progress_label.config(
                text=Context.get_text(
                    'execution_in_progress',
                    item_name=row[Constants.UI_TABLE_KEY_COL_NAME],
                    item_current_counter=item_current_counter,
                    item_total_counter=len(rows)
                )
            )

            # Show execution line for the current item
            LoggingHelper.log_info(
                message=Context.get_text(
                    'execution_in_progress',
                    item_name=row[Constants.UI_TABLE_KEY_COL_NAME],
                    item_current_counter=item_current_counter,
                    item_total_counter=len(rows)
                )
            )

            # Append id
            if row[Constants.UI_TABLE_KEY_COL_ID] not in self.__ids_dones:
                self.__ids_dones.append(
                    row[Constants.UI_TABLE_KEY_COL_ID]
                )

            # Waiting 0.1 seconde to see the dialog if the process is quick
            time.sleep(0.1)

            # If sub items enabled
            if self.__sub_items_enabled:
                # List sub items
                sub_items = self.list_sub_items(item=row)

                # Initialize sub progress bar
                self.__sub_progress_bar.config(maximum=len(sub_items))

                sub_item_current_counter = 1
                for sub_item in sub_items:

                    # Stop if execution stopped
                    if self.__stop_execution.is_set():
                        return

                    # Increment sub progress bar
                    self.__sub_progress_bar['value'] = sub_item_current_counter
                    self.__sub_progress_label.config(
                        text=Context.get_text(
                            'execution_in_progress',
                            item_name=sub_item[Constants.UI_TABLE_KEY_COL_NAME],
                            item_current_counter=sub_item_current_counter,
                            item_total_counter=len(sub_items)
                        )
                    )

                    # Show execution line for the current sub item
                    LoggingHelper.log_info(
                        message=Context.get_text(
                            'execution_in_progress',
                            item_name=sub_item[Constants.UI_TABLE_KEY_COL_NAME],
                            item_current_counter=sub_item_current_counter,
                            item_total_counter=len(sub_items)
                        )
                    )

                    # Waiting 0.1 seconde to see the dialog if the process is quick
                    time.sleep(0.1)

                    # Do execution for the current sub item
                    try:
                        self.do_execution(item=sub_item)
                    except Exception as exc:
                        LoggingHelper.log_error(
                            Context.get_text(
                                'error_execution',
                                item_name=sub_item[Constants.UI_TABLE_KEY_COL_NAME],
                                error=str(exc)
                            ),
                            exc
                        )

                        # Stop execution if error
                        self.__execution_finished = True
                        return

                    sub_item_current_counter += 1

                # Finish sub progression
                self.__sub_progress_bar['value'] = sub_item_current_counter
                self.__sub_progress_label.config(
                    text=''
                )
            else:
                # Append id
                if row[Constants.UI_TABLE_KEY_COL_ID] not in self.__ids_dones:
                    self.__ids_dones.append(
                        row[Constants.UI_TABLE_KEY_COL_ID]
                    )

                # Do execution for the current item
                try:
                    self.do_execution(item=row)
                except Exception as exc:
                    LoggingHelper.log_error(
                        Context.get_text(
                            'error_execution',
                            item_name=row[Constants.UI_TABLE_KEY_COL_NAME],
                            error=str(exc)
                        ),
                        exc
                    )

                    # Stop execution if error
                    self.__execution_finished = True
                    return

            item_current_counter += 1

        # Finish progression
        self.__progress_bar['value'] = item_current_counter
        self.__progress_label.config(
            text=Context.get_text('execution_finished')
        )

        # Show message for execution finished
        LoggingHelper.log_info(
            message=Context.get_text('execution_finished')
        )
        self.__execution_finished = True

        # Fix text Close for button to close
        self.__button_close.config(
            text=Context.get_text('close')
        )

    def get_ids_done(self) -> list:
        """Return ids done"""

        return self.__ids_dones

    @abstractmethod
    def get_category(self) -> Category:
        """Get Category"""

    @abstractmethod
    def get_action(self) -> Action:
        """Get Action"""

    @abstractmethod
    def list_sub_items(self, item: dict) -> list[dict]:
        """List sub items for the current item"""

    @abstractmethod
    def do_execution(self, item: dict):
        """Do execution for an item"""
