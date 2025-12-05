#!/usr/bin/python3
"""FrontEnd for BATOCERA"""

import os
from libraries.constants.constants import FrontEnd
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.frontend.abstract_frontend import AbstractFrontEnd
from libraries.xml.xml_helper import XmlHelper


class BatoceraFrontEnd(AbstractFrontEnd):
    """FrontEnd for BATOCERA"""

    __PATH_ROMS = 'roms'
    __PATH_GAMELIST = 'gamelist.xml'
    __PATH_BATOCERA = 'batocera.xml'

    __TAG_GAME = 'game'
    __TAG_NAME = 'name'

    def __init__(self):
        """Initialize FrontEnd"""

        super().__init__()

        self.__folder_path = Context.get_front_end_path(
            front_end=self.get_id()
        )

    def __retrieve_game_list_xml_path(
        self,
        platform: str
    ) -> str:
        """Retrieve the path for XML file listing games"""

        return os.path.join(
            self.__folder_path,
            self.__PATH_ROMS,
            platform,
            self.__PATH_GAMELIST
        )

    def get_id(self) -> FrontEnd:
        """Get id"""

        return FrontEnd.BATOCERA

    def list_platforms(self) -> list:
        """List platforms"""

        platforms = []
        for platform in FileHelper.list_sub_directories(
            folder_path=os.path.join(
                self.__folder_path,
                self.__PATH_ROMS
            )
        ):
            if not FileHelper.is_file_exists(
                self.__retrieve_game_list_xml_path(
                    platform=platform
                )
            ):
                continue

            platforms.append(platform)

        return platforms

    def list_games(self, platform: str) -> list:
        """List games"""

        games = XmlHelper.list_tag_values(
            xml_file_path=os.path.join(
                self.__retrieve_game_list_xml_path(
                    platform=platform
                )
            ),
            parent_tag=self.__TAG_GAME,
            tag=self.__TAG_NAME
        )

        return games

    def do_export(
        self,
        game_id: str,
        game_name: str
    ):
        """Do export for a plateform and a game"""

        if not FileHelper.is_file_exists(
            os.path.join(
                self.__retrieve_game_list_xml_path(
                    platform=Context.get_selected_platform()
                )
            )
        ):
            raise Exception(f'Cannot find {self.__PATH_GAMELIST}')

        game_xml_node = XmlHelper.retrieve_node(
            xml_file_path=os.path.join(
                self.__retrieve_game_list_xml_path(
                    platform=Context.get_selected_platform()
                )
            ),
            tag=self.__TAG_GAME,
            field_id=self.__TAG_NAME,
            field_value=game_name
        )

        XmlHelper.write_node(
            xml_file_path=os.path.join(
                Context.get_games_path(),
                Context.get_selected_platform(),
                game_id,
                self.__PATH_BATOCERA
            ),
            node=game_xml_node
        )
