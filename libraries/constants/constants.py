#!/usr/bin/python3
"""Constants"""

from enum import Enum


class Action(Enum):
    """Action"""

    INSTALL = 'action_install'
    UNINSTALL = 'action_uninstall'
    EXPORT = 'action_export'
    COPY = 'action_copy'
    EDIT = 'action_edit'


class Constants:
    """Class to store constants"""

    # Constants for paths
    RESOURCES_PATH = 'resources'

    # Constants for cache
    CACHE_FILES_NAMES = [
        'thumb',
        'pthumbs',
        'Thumbs'
    ]

    # Constants for UI
    UI_PAD_SMALL = 5
    UI_PAD_BIG = 10

    # Constants for setup
    SETUP_LANG_CODE = 'lang_code'
    SETUP_MONITOR = 'monitor'
    SETUP_SIMULATED = 'simulated'

    # Constants for item color
    ITEM_COLOR_BLACK = 'black'
    ITEM_COLOR_GREEN = 'green'
    ITEM_COLOR_ORANGE = 'orange'
    ITEM_COLOR_RED = 'red'
