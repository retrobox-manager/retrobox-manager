#!/usr/bin/python3
"""Context"""

from dataclasses import dataclass
import sys
import os
from pathlib import Path
import re
import socket
import configparser
import locale

from libraries.constants.constants import Action, Category, Component, \
    Constants, Media, SoftwareId

# pylint: disable=unnecessary-comprehension
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-branches
# pylint: disable=protected-access


@dataclass
class SoftwareContext:
    """
    Represents the configuration context of a software.
    """

    enabled: bool
    path: str

    # sources: source_id -> software_id
    sources: dict[str, SoftwareId]

    # platform_name -> roms_folder
    platform_associations: dict[str, str]

    # media_enum -> resource_name
    media_associations: dict[Media, str]

    # (row, column) -> media_enum
    media_positions: dict[tuple[int, int], Media]

    def __init__(self):
        """
        Initialize a SoftwareContext with empty/default values.
        """
        self.enabled = False
        self.path = ""
        self.sources = {}
        self.platform_associations = {}
        self.media_associations = {}
        self.media_positions = {}


class Context:
    """Class to store context"""

    __initialized: bool = False
    __hostname: str = None
    __app_version: str = None
    __texts_by_lang_code = {}
    __working_path = None
    __base_path = None
    __packaged = False
    __selected_category: Category = None
    __selected_action: Action = None
    __selected_platform: str = None
    __selected_software: SoftwareId = None
    __selected_rows = []
    __selected_components = []
    __selected_folder_path = None
    __lang_code: str = 'fr' if locale.getlocale()[0].startswith('fr') else 'en'
    __monitor: int = 0
    __simulated: bool = False
    __platforms: list[str] = []
    __software_context_map: dict[SoftwareId, SoftwareContext] = {}

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
        retrobox_manager_path = os.getenv("RETROBOX_MANAGER_PATH")
        if retrobox_manager_path is not None:
            Context.__working_path = retrobox_manager_path
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
                Constants.PATH_RESOURCES,
                'lang',
                f'messages_{lang_code}.properties'
            )
            with open(lang_path, encoding='utf-8') as file:
                texts_properties.read_file(file)
            Context.__texts_by_lang_code[lang_code] = {
                key: value for key, value in texts_properties.items('DEFAULT')
            }

        # Initialize contexts for each software
        Context.__software_context_map = {
            software_id: SoftwareContext()
            for software_id in SoftwareId
        }

        # Specify that context is initialized
        Context.__initialized = True

        # Create the games directory if it doesn't exist
        if not os.path.exists(Context.get_games_path()):
            os.makedirs(Context.get_games_path())

        # Create the configs directory if it doesn't exist
        if not os.path.exists(Context.get_configs_path()):
            os.makedirs(Context.get_configs_path())

        # Create the setup directory if it doesn't exist
        if not os.path.exists(Context.get_setup_path()):
            os.makedirs(Context.get_setup_path())

        # Create the cache directory if it doesn't exist
        if not os.path.exists(Context.get_cache_path()):
            os.makedirs(Context.get_cache_path())

    @staticmethod
    def destroy():
        """Destroy context"""

        if Context.__initialized:
            Context.__initialized = False

    @staticmethod
    def get_lang_code() -> str:
        """Get lang's code"""

        if not Context.__initialized:
            Context.init()

        return Context.__lang_code

    @staticmethod
    def get_monitor() -> int:
        """Get monitor"""

        if not Context.__initialized:
            Context.init()

        return Context.__monitor

    @staticmethod
    def is_simulated() -> bool:
        """Specify if simulated"""

        if not Context.__initialized:
            Context.init()

        return Context.__simulated

    @staticmethod
    def get_software_context(software_id: SoftwareId) -> SoftwareContext:
        """Get SoftwareContext for the specified software"""

        if not Context.__initialized:
            Context.init()

        return Context.__software_context_map[software_id]

    @staticmethod
    def set_setup(setup: dict):
        """Set setup"""

        if not Context.__initialized:
            Context.init()

        # Update general context from setup
        general_setup = setup[Constants.SETUP_TAG_GENERAL]
        Context.__lang_code: str = general_setup[Constants.SETUP_TAG_LANG_CODE]
        Context.__monitor: int = general_setup[Constants.SETUP_TAG_MONITOR]
        Context.__simulated: bool = general_setup[Constants.SETUP_TAG_SIMULATED]
        Context.__platforms: list[str] = []
        for platform in setup[Constants.SETUP_TAG_PLATFORMS]:
            Context.__platforms.append(platform)

        # Update context for each software
        for software_config in setup[Constants.SETUP_TAG_SOFTWARES]:
            software_id = SoftwareId[software_config[Constants.SETUP_TAG_ID]]
            software_context = Context.__software_context_map[software_id]

            # Reinitialize software context if disabled
            if not software_config[Constants.SETUP_TAG_ENABLED]:
                Context.__software_context_map[software_id] = SoftwareContext()
                continue

            software_context.enabled = True
            software_context.path = software_config[Constants.SETUP_TAG_PATH]

            # Set sources
            sources: dict[str, SoftwareId] = {}
            for setup_source in software_config[Constants.SETUP_TAG_SOURCES]:
                sources[setup_source[Constants.SETUP_TAG_ID]] = SoftwareId[
                    setup_source[Constants.SETUP_TAG_SOFTWARE]
                ]
            software_context.sources = sources

            # Set platform_associations
            platform_associations: dict[str, str] = {}
            for setup_associations in software_config[
                Constants.SETUP_TAG_PLATFORM_ASSOCIATIONS
            ]:
                platform_associations[
                    setup_associations[Constants.SETUP_TAG_PLATFORM]
                ] = setup_associations[Constants.SETUP_TAG_ROMS_FOLDER]
            software_context.platform_associations = platform_associations

            # Set media_associations
            media_associations: dict[Media, str] = {}
            for setup_associations in software_config[
                Constants.SETUP_TAG_MEDIA_ASSOCIATIONS
            ]:
                media_associations[
                    Media[setup_associations[Constants.SETUP_TAG_MEDIA]]
                ] = setup_associations[Constants.SETUP_TAG_RESOURCE]
            software_context.media_associations = media_associations

            # Set media_positions
            media_positions: dict[tuple[int, int], Media] = {}
            for setup_positions in software_config[
                Constants.SETUP_TAG_MEDIA_POSITIONS
            ]:
                media_positions[
                    (
                        setup_positions[Constants.SETUP_TAG_ROW],
                        setup_positions[Constants.SETUP_TAG_COLUMN]
                    )
                ] = Media[setup_positions[Constants.SETUP_TAG_MEDIA]]
            software_context.media_positions = media_positions

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
    def get_text(text_id: str, lang=None, **kwargs) -> str:
        """Get text from its id"""

        if not Context.__initialized:
            Context.init()

        if lang is None:
            lang = Context.__lang_code

        return Context.__texts_by_lang_code[lang][text_id].format(**kwargs)

    @staticmethod
    def get_selected_rows_cache_path():
        """Get cache path describing rows for selection"""

        file_name = 'rows_'
        file_name += Context.get_selected_category().value.split('_')[
            1].lower()
        if Context.get_selected_action() not in [Action.DELETE, Action.EDIT]:
            file_name += '_'
            file_name += Context.get_selected_software().value.lower()
        if Context.get_selected_category() == Category.GAMES:
            file_name += '_'
            file_name += Context.get_selected_platform().replace(' ', '_').lower()
        file_name += '_'
        file_name += Context.get_selected_action().value.split('_')[1].lower()
        return Path(os.path.join(
            Context.get_cache_path(),
            f'{file_name}{Constants.XML_EXTENSION}'
        ))

    @staticmethod
    def get_setup_file_path() -> Path:
        """Get setup file path"""

        if not Context.__initialized:
            Context.init()

        return Path(os.path.join(
            Context.get_setup_path(),
            f'{Context.get_hostname()}{Constants.XML_EXTENSION}'
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
    def get_games_path() -> Path:
        """Get games path"""

        if not Context.__initialized:
            Context.init()

        return Path(os.path.join(
            Context.get_working_path(),
            'games'
        ))

    @staticmethod
    def get_configs_path() -> Path:
        """Get configs path"""

        if not Context.__initialized:
            Context.init()

        return Path(os.path.join(
            Context.get_working_path(),
            'configs'
        ))

    @staticmethod
    def get_setup_path() -> Path:
        """Get setup path"""

        if not Context.__initialized:
            Context.init()

        return Path(os.path.join(
            Context.get_working_path(),
            'setup'
        ))

    @staticmethod
    def is_packaged() -> bool:
        """Specify if app is packaged"""

        if not Context.__initialized:
            Context.init()

        return Context.__packaged

    @staticmethod
    def get_selected_category() -> Category:
        """Get selected category"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_category

    @staticmethod
    def set_selected_category(category: Category):
        """Set selected category"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_category = category

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
    def get_selected_platform() -> str:
        """Get selected platform"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_platform

    @staticmethod
    def set_selected_platform(platform: str):
        """Set selected platform"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_platform = platform

    @staticmethod
    def get_selected_software() -> SoftwareId:
        """Get selected software"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_software

    @staticmethod
    def set_selected_software(software: SoftwareId):
        """Set selected software"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_software = software

    @staticmethod
    def list_available_platforms() -> list[str]:
        """List available platforms"""

        if not Context.__initialized:
            Context.init()

        return Context.__platforms

    @staticmethod
    def list_available_softwares() -> list[SoftwareId]:
        """List available softwares"""

        if not Context.__initialized:
            Context.init()

        result = []
        for software_id, software_context in Context.__software_context_map.items():
            if software_context.enabled:
                result.append(software_id)

        return result

    @staticmethod
    def get_selected_rows() -> list:
        """Get selected rows"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_rows

    @staticmethod
    def set_selected_rows(rows: list):
        """Set selected rows"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_rows = rows

    @staticmethod
    def get_selected_components() -> list[Component]:
        """Get selected components"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_components

    @staticmethod
    def set_selected_components(components_items: list):
        """Set selected components"""

        if not Context.__initialized:
            Context.init()

        components_labels = []
        for components_item in components_items:
            components_labels.append(
                components_item[Constants.UI_TABLE_KEY_COL_NAME]
            )

        result = []
        for component in Component:
            if Context.get_text(component.value) in components_labels:
                result.append(component)

        Context.__selected_components = result

    @staticmethod
    def get_selected_folder_path() -> str:
        """Get selected folder's path"""

        if not Context.__initialized:
            Context.init()

        return Context.__selected_folder_path

    @staticmethod
    def set_selected_folder_path(folder_path: str):
        """Set selected folder's path"""

        if not Context.__initialized:
            Context.init()

        Context.__selected_folder_path = folder_path
