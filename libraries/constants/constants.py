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


class FrontEnd(Enum):
    """FrontEnd"""

    BATOCERA = 'Batocera'
    LAUNCHBOX = 'LaunchBox / BigBox'


class Scraper(Enum):
    """Scraper"""

    EMU_MOVIES = 'EmuMovies'
    SKRAPER = 'Skraper'


class Constants:
    """Class to store constants"""

    # Constants for paths
    RESOURCES_PATH = 'resources'
    GAMES_PATH = 'games'
    BATOCERA_ROMS_PATH = 'roms'
    BATOCERA_GAMELIST_PATH = 'gamelist.xml'
    LAUNCHBOX_DATA_PATH = 'Data'
    LAUNCHBOX_IMAGES_PATH = 'Images'
    LAUNCHBOX_VIDEOS_PATH = 'Videos'
    LAUNCHBOX_PLATFORMS_PATH = 'Platforms'

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

    # Constants for setup
    SETUP_LANG_CODE = 'lang_code'
    SETUP_MONITOR = 'monitor'
    SETUP_SIMULATED = 'simulated'
    SETUP_AVAILABLE_FRONT_ENDS = 'available_front_ends'
    SETUP_FRONT_END_BATOCERA_PATH = 'front_end_batocera_path'
    SETUP_FRONT_END_LAUNCHBOX_PATH = 'front_end_launchbox_path'
    SETUP_AVAILABLE_SCRAPERS = 'available_scrapers'
    SETUP_SCRAPER_EMU_MOVIES_PATH = 'scraper_emu_movies_path'
    SETUP_SCRAPER_SKRAPER_PATH = 'scraper_skraper_path'

    # Constants for item color
    ITEM_COLOR_BLACK = 'black'
    ITEM_COLOR_GREEN = 'green'
    ITEM_COLOR_ORANGE = 'orange'
    ITEM_COLOR_RED = 'red'
