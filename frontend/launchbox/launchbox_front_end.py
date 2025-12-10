#!/usr/bin/python3
"""FrontEnd for LAUNCHBOX"""

import os
from libraries.constants.constants import Constants, FrontEnd
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.xml.xml_helper import XmlHelper
from frontend.abstract_frontend import AbstractFrontEnd


class LaunchboxFrontEnd(AbstractFrontEnd):
    """FrontEnd for LAUNCHBOX"""

    __PATH_DATA = 'Data'
    __PATH_PLATFORMS = 'Platforms'

    def __init__(self):
        """Initialize FrontEnd"""

        self.__folder_path = Context.get_front_end_path(
            front_end=self.get_enum()
        )

    def get_enum(self) -> FrontEnd:
        """Get enum"""

        return FrontEnd.LAUNCHBOX

    def get_id(self) -> str:
        """Get id"""

        return self.get_enum().value.lower()

    def get_rom_key(self) -> str:
        """Get rom's key"""

        return ''

    def list_platforms(self) -> list:
        """List platforms"""

        platforms = []
        for relative_path in FileHelper.list_relative_paths(
            folder_path=os.path.join(
                self.__folder_path,
                self.__PATH_DATA,
                self.__PATH_PLATFORMS
            ),
            file_name='*',
            error_if_not_found=False
        ):
            if not relative_path.endswith(Constants.XML_EXTENSION):
                continue
            platforms.append(
                relative_path[:-len(Constants.XML_EXTENSION)]
            )

        return platforms

    def list_games(self, platform: str) -> list:
        """List games"""

        games = XmlHelper.list_tag_values(
            xml_file_path=os.path.join(
                self.__folder_path,
                self.__PATH_DATA,
                self.__PATH_PLATFORMS,
                f'{platform}{Constants.XML_EXTENSION}'
            ),
            parent_tag='Game',
            tag='Title'
        )
        return games

    def retrieve_game_files(self, platform: str, game: str) -> dict:
        """Retrieve game files"""

        print(platform)
        print(game)

        return {}

    def retrieve_game_info(self, platform: str, game: str) -> str:
        """Retrieve game info"""

        print(platform)
        print(game)

        return ''
