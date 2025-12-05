#!/usr/bin/python3
"""Abstract FrontEnd"""

from abc import ABC, abstractmethod
import threading
import tkinter as tk
from tkinter import ttk

from libraries.constants.constants import Action, Constants, FrontEnd
from libraries.context.context import Context
from libraries.logging.logging_helper import LoggingHelper


class AbstractFrontEnd(ABC):
    """Abstract FrontEnd (Common for all frontends)"""

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
                    Context.get_selected_action().value
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
                match(Context.get_selected_action()):
                    case Action.EXPORT:
                        self.do_export(
                            game_id=row[Constants.UI_TABLE_KEY_COL_ID],
                            game_name=row[Constants.UI_TABLE_KEY_COL_NAME]
                        )

                    case _:
                        raise Exception('Not implemented action!')
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
    def do_export(
        self,
        game_id: str,
        game_name: str
    ):
        """Do export for a plateform and a game"""

    @abstractmethod
    def get_id(self) -> FrontEnd:
        """Get id"""

    @abstractmethod
    def list_platforms(self) -> list:
        """List platforms"""

    @abstractmethod
    def list_games(self, platform: str) -> list:
        """List games"""
