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


class Platform(Enum):
    """Platform"""

    SEGA_MASTERSYSTEM = 'Sega Master System'
    SEGA_MEGADRIVE = 'Sega Megadrive'


class Media(Enum):
    """Media"""

    BOX_2D_FRONT = 'box_2d_front'
    BOX_2D_SIDE = 'box_2d_side'
    BOX_2D_BACK = 'box_2d_back'
    BOX_3D = 'box_3d'
    SUPPORT = 'support'
    FAN_ART = 'fan_art'
    SCREENSHOT_GAME = 'screenshot_game'
    SCREENSHOT_TITLE = 'screenshot_title'
    LOGO = 'logo'
    LOGO_CARBON = 'logo_carbon'
    LOGO_STEEL = 'logo_steel'
    BEZEL = 'bezel'
    MANUAL = 'manual'
    VIDEO = 'video'


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
    UI_TABLE_KEY_COL_ROM = 'column_title_rom'
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
