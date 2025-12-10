#!/usr/bin/python3
"""Constants"""

from enum import Enum


class Category(Enum):
    """Category"""

    GAMES = 'category_games'
    CONFIGS = 'category_configs'


class Action(Enum):
    """Action"""

    INSTALL = 'action_install'
    UNINSTALL = 'action_uninstall'
    EXPORT = 'action_export'
    COPY = 'action_copy'
    EDIT = 'action_edit'


class Software(Enum):
    """Software"""

    BATOCERA = 'Batocera'
    LAUNCHBOX = 'LaunchBox'
    EMU_MOVIES = 'EmuMovies'
    SKRAPER = 'Skraper'


class Media(Enum):
    """Media"""

    BOX_2D_FRONT = 'media_box_2d_front'
    BOX_2D_SIDE = 'media_box_2d_side'
    BOX_2D_BACK = 'media_box_2d_back'
    BOX_3D = 'media_box_3d'
    SUPPORT = 'media_support'
    FAN_ART = 'media_fan_art'
    SCREENSHOT_GAME = 'media_screenshot_game'
    SCREENSHOT_TITLE = 'media_screenshot_title'
    LOGO = 'media_logo'
    LOGO_CARBON = 'media_logo_carbon'
    LOGO_STEEL = 'media_logo_steel'
    MANUAL = 'media_manual'
    VIDEO = 'media_video'


class Constants:
    """Class to store constants"""

    # Constants for paths
    RESOURCES_PATH = 'resources'
    GAMES_PATH = 'games'

    # Constants for extensions
    XML_EXTENSION = '.xml'

    # Constants for cache
    CACHE_FILES_NAMES = [
        'thumb',
        'pthumbs',
        'Thumbs'
    ]

    # Constants for UI
    UI_PAD_SMALL = 5
    UI_PAD_BIG = 10
    UI_TABLE_KEY_COL_SELECTION = 'column_title_selection'
    UI_TABLE_KEY_COL_ID = 'column_title_id'
    UI_TABLE_KEY_COL_NAME = 'column_title_name'
    UI_TABLE_KEY_COLOR = 'color'

    # Constants for setup
    SETUP_LANG_CODE = 'lang_code'
    SETUP_MONITOR = 'monitor'
    SETUP_SIMULATED = 'simulated'
    SETUP_AVAILABLE_SOFTWARES = 'available_softwares'
    SETUP_SOFTWARE_BATOCERA_PATH = 'software_batocera_path'
    SETUP_SOFTWARE_LAUNCHBOX_PATH = 'software_launchbox_path'
    SETUP_SOFTWARE_EMU_MOVIES_PATH = 'software_emu_movies_path'
    SETUP_SOFTWARE_SKRAPER_PATH = 'software_skraper_path'

    # Constants for item color
    ITEM_COLOR_BLACK = 'black'
    ITEM_COLOR_GREEN = 'green'
    ITEM_COLOR_ORANGE = 'orange'
    ITEM_COLOR_RED = 'red'
