#!/usr/bin/python3
"""Abstract Executor"""

from abc import ABC, abstractmethod
import threading
import tkinter as tk
from tkinter import ttk

from libraries.constants.constants import Action, Category, Constants
from libraries.context.context import Context
from libraries.logging.logging_helper import LoggingHelper


class AbstractExecutor(ABC):
    """Abstract Executor (Common for all executors)"""

    def __init__(
        self
    ):
        """Initialize executor"""

        self.__execution_finished: bool = False
        self.__stop_execution = threading.Event()
        self.__progress_bar = None
        self.__progress_label = None
        self.__button_close = None

    def set_ui_components(
        self,
        progress_bar: ttk.Progressbar,
        progress_label: tk.Label,
        button_close: tk.Button
    ):
        """Set UI Components"""

        self.__progress_bar = progress_bar
        self.__progress_label = progress_label
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

            # Continue if execution stopped
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

    @abstractmethod
    def get_category(self) -> Category:
        """Get Category"""

    @abstractmethod
    def get_action(self) -> Action:
        """Get Action"""

    @abstractmethod
    def do_execution(self, item: dict):
        """Do execution for an item"""
