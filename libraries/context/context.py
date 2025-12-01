#!/usr/bin/python3
"""Context"""

import sys
import os
from pathlib import Path
import re
import socket
import configparser
import locale

from libraries.constants.constants import Action, Constants

# pylint: disable=unnecessary-comprehension
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-branches
# pylint: disable=protected-access


class Context:
    """Class to store context"""

    __initialized: bool = False
    __hostname: str = None
    __app_version: str = None
    __lang_code: str = None
    __monitor: int = None
    __texts_by_lang_code = {}
    __simulated: bool = False
    __working_path = None
    __base_path = None
    __packaged = False
    __selected_action: Action = None

    @staticmethod
    def init():
        """Initialize context"""

        if Context.__initialized:
            raise Exception(Context.get_text(
                'error_context_initialized'
            ))

        # Retrieve hostname
        Context.__hostname = socket.gethostname().lower()

        # Define working path
        pincab_manager_path = os.getenv("PINCAB_MANAGER_PATH")
        if pincab_manager_path is not None:
            Context.__working_path = pincab_manager_path
        else:
            Context.__working_path = os.getcwd()

        # Define base path depending on DEV or package
        try:
            Context.__base_path = sys._MEIPASS
            Context.__packaged = True
        except AttributeError:
            Context.__base_path = os.getcwd()
            Context.__packaged = False

        # Retrieve application's version
        try:
            with open(Context.__base_path + '/CHANGELOG', 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()
                match = re.search(r'R(\d+\.\d+\.\d+)', first_line)
                if not match:
                    raise Exception('Cannot find app_version in CHANGELOG')
                Context.__app_version = match.group(1)
        except Exception:
            Context.__app_version = 'UNKNOWN'

        # Retrieve text for each lang
        texts_properties = configparser.ConfigParser()
        for lang_code in ['fr', 'en']:
            lang_path = os.path.join(
                Context.__base_path,
                Constants.RESOURCES_PATH,
                'lang',
                f'messages_{lang_code}.properties'
            )
            with open(lang_path, encoding='utf-8') as file:
                texts_properties.read_file(file)
            Context.__texts_by_lang_code[lang_code] = {
                key: value for key, value in texts_properties.items('DEFAULT')
            }

        # Retrieve lang's code from OS language
        lang = locale.getlocale()[0]
        Context.__lang_code = 'fr' if lang.startswith('fr') else 'en'

        # Initialize monitor
        Context.__monitor = 0

        # Initialize boolean simulated
        Context.__simulated = False

        # Specify that context is initialized
        Context.__initialized = True

        # Update context from setup
        Context.update_context_from_setup()

    @staticmethod
    def destroy():
        """Destroy context"""

        if Context.__initialized:
            Context.__initialized = False

    @staticmethod
    def get_hostname() -> str:
        """Get hostname"""

        if not Context.__initialized:
            Context.init()

        return Context.__hostname

    @staticmethod
    def get_working_path() -> str:
        """Get working path"""

        if not Context.__initialized:
            Context.init()

        return Context.__working_path

    @staticmethod
    def get_base_path() -> str:
        """Get base path"""

        if not Context.__initialized:
            Context.init()

        return Context.__base_path

    @staticmethod
    def get_app_version() -> str:
        """Get application's version"""

        if not Context.__initialized:
            Context.init()

        return Context.__app_version

    @staticmethod
    def get_lang_code() -> str:
        """Get lang code"""

        if not Context.__initialized:
            Context.init()

        return Context.__lang_code

    @staticmethod
    def get_text(text_id: str, lang=None, **kwargs) -> str:
        """Get text from its id"""

        if not Context.__initialized:
            Context.init()

        if lang is None:
            lang = Context.get_lang_code()

        return Context.__texts_by_lang_code[lang][text_id].format(**kwargs)

    @staticmethod
    def get_monitor() -> int:
        """Get monitor"""

        if not Context.__initialized:
            Context.init()

        return Context.__monitor

    @staticmethod
    def get_setup_file_path() -> Path:
        """Get setup file path"""

        if not Context.__initialized:
            Context.init()

        return Path(os.path.join(
            Context.get_working_path(),
            'setup',
            f'{Context.get_hostname()}.cfg'
        ))

    @staticmethod
    def get_logs_path() -> Path:
        """Get logs path"""

        if not Context.__initialized:
            Context.init()

        return Path(os.path.join(
            Context.get_working_path(),
            'logs'
        ))

    @staticmethod
    def get_cache_path():
        """Get cache path"""

        if not Context.__initialized:
            Context.init()

        return Path(os.path.join(
            Context.get_working_path(),
            'cache'
        ))

    @staticmethod
    def is_packaged() -> bool:
        """Specify if app is packaged"""

        if not Context.__initialized:
            Context.init()

        return Context.__packaged

    @staticmethod
    def is_simulated() -> bool:
        """Specify if app is simulated"""

        if not Context.__initialized:
            Context.init()

        return Context.__simulated

    @staticmethod
    def get_selected_action() -> Action:
        """Get selected action"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_action

    @staticmethod
    def set_selected_action(action: Action):
        """Set selected action"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_action = action

    @staticmethod
    def update_context_from_setup():
        """Update context from setup"""

        if not Context.__initialized:
            Context.init()

        # If setup file exists, retrieve context from it
        if Context.get_setup_file_path().exists():
            setup = configparser.ConfigParser()
            with open(Context.get_setup_file_path(), encoding='utf-8') as file:
                setup.read_file(file)

            setup_items = {
                key: value for key, value in setup.items('DEFAULT')
            }
            if Constants.SETUP_LANG_CODE in setup_items:
                Context.__lang_code = setup_items[
                    Constants.SETUP_LANG_CODE
                ]

            if Constants.SETUP_MONITOR in setup_items:
                Context.__monitor = int(setup_items[
                    Constants.SETUP_MONITOR
                ])

            if Constants.SETUP_SIMULATED in setup_items:
                Context.__simulated = setup_items[
                    Constants.SETUP_SIMULATED
                ] == 'True'
