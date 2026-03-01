#!/usr/bin/python3
"""Constants"""

from enum import Enum


class Category(Enum):
    """Category"""

    PLATFORMS = 'category_platforms'
    GAMES = 'category_games'
    CONFIGS = 'category_configs'


class Component(Enum):
    """Component"""

    INFO = 'component_info'
    ROM = 'component_rom'
    MEDIA = 'component_media'
    FILES = 'component_files'
    REGISTRY = 'component_registry'


class Action(Enum):
    """Action"""

    INSTALL = 'action_install'
    UNINSTALL = 'action_uninstall'
    EXPORT = 'action_export'
    COPY = 'action_copy'
    EDIT = 'action_edit'
    VIEW = 'action_view'
    DELETE = 'action_delete'


class SoftwareId(Enum):
    """Software id"""

    BATOCERA = 'Batocera'
    LAUNCHBOX = 'LaunchBox'
    EMU_MOVIES = 'EmuMovies'
    SKRAPER = 'Skraper'


class Media(Enum):
    """Media"""

    BEZEL = 'media_bezel'
    BOX_2D_FRONT = 'media_box_2d_front'
    BOX_2D_SIDE = 'media_box_2d_side'
    BOX_2D_BACK = 'media_box_2d_back'
    BOX_2D = 'media_box_2d'
    BOX_3D = 'media_box_3d'
    FAN_ART = 'media_fan_art'
    LOGO = 'media_logo'
    LOGO_CARBON = 'media_logo_carbon'
    LOGO_STEEL = 'media_logo_steel'
    SCREENSHOT_MIX = 'media_screenshot_mix'
    SCREENSHOT_GAME = 'media_screenshot_game'
    SCREENSHOT_TITLE = 'media_screenshot_title'
    SUPPORT = 'media_support'
    MANUAL = 'media_manual'
    VIDEO = 'media_video'


class Constants:
    """Class to store constants"""

    # --- Default platform names (strings only) ---
    DEFAULT_PLATFORM_ATARI_2600 = 'Atari 2600'
    DEFAULT_PLATFORM_ATARI_7800 = 'Atari 7800'
    DEFAULT_PLATFORM_MICROSOFT_XBOX360 = 'Microsoft Xbox 360'
    DEFAULT_PLATFORM_NINTENDO_64 = 'Nintendo 64'
    DEFAULT_PLATFORM_NINTENDO_GAMEBOY_ADVANCE = 'Nintendo GameBoy Advance'
    DEFAULT_PLATFORM_NINTENDO_GAMECUBE = 'Nintendo GameCube'
    DEFAULT_PLATFORM_NINTENDO_NES = 'Nintendo NES'
    DEFAULT_PLATFORM_NINTENDO_SNES = 'Nintendo SNES'
    DEFAULT_PLATFORM_NINTENDO_SWITCH = 'Nintendo Switch'
    DEFAULT_PLATFORM_NINTENDO_WII = 'Nintendo Wii'
    DEFAULT_PLATFORM_PC = 'PC'
    DEFAULT_PLATFORM_SEGA_DREAMCAST = 'Sega Dreamcast'
    DEFAULT_PLATFORM_SEGA_GAMEGEAR = 'Sega Game Gear'
    DEFAULT_PLATFORM_SEGA_MASTERSYSTEM = 'Sega Master System'
    DEFAULT_PLATFORM_SEGA_MEGADRIVE = 'Sega Megadrive'
    DEFAULT_PLATFORM_SNK_NEOGEO = 'SNK Neo-Geo'
    DEFAULT_PLATFORM_SONY_PLAYSTATION_2 = 'Sony Playstation 2'
    DEFAULT_PLATFORM_SONY_PSP = 'Sony PSP'

    # --- List of default platform names ---
    DEFAULT_PLATFORMS = [
        value
        for name, value in vars().items()
        if name.startswith('DEFAULT_PLATFORM_')
    ]

    # Constants for paths
    PATH_RESOURCES = 'resources'
    PATH_GAMES = 'games'
    PATH_ROM = 'rom'
    PATH_MEDIA = 'media'

    # Constants for cache
    CACHE_TAG_ROOT = 'rows'

    # Constants for UI
    UI_PAD_SMALL = 5
    UI_PAD_BIG = 10
    UI_TABLE_KEY_COL_SELECTION = 'column_title_selection'
    UI_TABLE_KEY_COL_ID = 'column_title_id'
    UI_TABLE_KEY_COL_NAME = 'column_title_name'
    UI_TABLE_KEY_COL_ROMS_FOLDER = 'column_title_roms_folder'
    UI_TABLE_KEY_COL_PLATFORM = 'column_title_platform'
    UI_TABLE_KEY_COL_ROM = 'column_title_rom'
    UI_TABLE_KEY_COL_GAMES = 'column_title_games'
    UI_TABLE_KEY_COL_UNIQUE = 'column_title_unique'
    UI_TABLE_KEY_COL_RESOURCE = 'column_title_resource'
    UI_TABLE_KEY_COL_MEDIA = 'column_title_media'
    UI_TABLE_KEY_COLOR = 'color'

    # Constants for setup
    SETUP_TAG_ROOT = 'config'
    SETUP_TAG_GENERAL = 'general'
    SETUP_TAG_SOFTWARES = 'softwares'
    SETUP_TAG_SOFTWARE = 'software'
    SETUP_TAG_LANG_CODE = 'lang_code'
    SETUP_TAG_MONITOR = 'monitor'
    SETUP_TAG_SIMULATED = 'simulated'
    SETUP_TAG_ID = 'id'
    SETUP_TAG_ENABLED = 'enabled'
    SETUP_TAG_PATH = 'path'
    SETUP_TAG_SOURCES = 'sources'
    SETUP_TAG_SOURCE = 'source'
    SETUP_TAG_PLATFORMS = 'platforms'
    SETUP_TAG_PLATFORM_ASSOCIATIONS = 'platform_associations'
    SETUP_TAG_MEDIA_ASSOCIATIONS = 'media_associations'
    SETUP_TAG_MEDIA_POSITIONS = 'media_positions'
    SETUP_TAG_MEDIA = 'media'
    SETUP_TAG_RESOURCE = 'resource'
    SETUP_TAG_ROW = 'row'
    SETUP_TAG_COLUMN = 'column'
    SETUP_TAG_PLATFORM = 'platform'
    SETUP_TAG_ROMS_FOLDER = 'roms_folder'
    SETUP_SOURCE_GAME_INFO = 'game_info'

    # Constants for extensions
    XML_EXTENSION = '.xml'
    PDF_EXTENSION = '.pdf'
    REG_EXTENSION = '.reg'

    # Constants for item color
    ITEM_COLOR_BLACK = 'black'
    ITEM_COLOR_GREEN = 'green'
    ITEM_COLOR_ORANGE = 'orange'
    ITEM_COLOR_RED = 'red'

    # Regedit constants
    REGEDIT_ROOT_KEY_NAME = 'HKEY_CURRENT_USER'
    REGEDIT_KEY_SEPARATOR = '\\'
    REGEDIT_FILE_ENCODING = 'UTF-8'

    # Constants for VLC
    VLC_SUPPORTED_EXTENSIONS = {
        # Video
        '.mp4', '.m4v', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
        '.mpg', '.mpeg', '.mpe', '.3gp', '.3g2', '.ogv', '.asf', '.ts',
        '.m2ts', '.dv', '.rmvb', '.vob', '.hevc', '.h265',
        # Audio
        '.mp3', '.flac', '.wav', '.aac', '.ogg', '.wma', '.m4a', '.caf',
        '.opus', '.midi', '.mid', '.ape', '.dsf', '.dff',
        # Image
        '.jpg', '.jpeg', '.apng', '.png', '.bmp', '.gif', '.tiff'
    }
