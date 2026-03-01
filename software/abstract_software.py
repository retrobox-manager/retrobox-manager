#!/usr/bin/python3
"""Abstract Software"""

import os

from typing import Type, Dict, Self

from abc import ABC, abstractmethod

from libraries.constants.constants import Media, SoftwareId, Constants
from libraries.context.context import Context, SoftwareContext
from libraries.file.file_helper import FileHelper

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-public-methods


class AbstractSoftware(ABC):
    """Abstract software (Common for all softwares)"""

    # Map containing registered softwares
    __registered_softwares: Dict[SoftwareId, Type[Self]] = {}

    @classmethod
    def register_software(
        cls,
        software_id: SoftwareId,
        subclass: Type[Self]
    ) -> None:
        """
        Register a concrete software implementation.

        Args:
            software_id (SoftwareId):
                Enum identifier associated with the software.

            subclass (Type[AbstractSoftware]):
                Concrete class inheriting from AbstractSoftware.

        Raises:
            TypeError:
                If subclass does not inherit from AbstractSoftware.
        """
        if not issubclass(subclass, AbstractSoftware):
            raise TypeError(
                f"{subclass.__name__} must inherit from AbstractSoftware"
            )

        cls.__registered_softwares[software_id] = subclass

    @classmethod
    def get_registered_software(
        cls,
        software_id: SoftwareId,
        *args,
        **kwargs
    ) -> Self:
        """
        Get registered software.

        Args:
            software_id (SoftwareId):
                Enum identifier of the software to instantiate.

            *args:
                Positional arguments forwarded to the constructor.

            **kwargs:
                Keyword arguments forwarded to the constructor.

        Returns:
            AbstractSoftware:
                An instance of the requested software.

        Raises:
            ValueError:
                If no software is registered for the given type.
        """

        if software_id not in cls.__registered_softwares:
            raise ValueError(
                f"No software registered for {software_id}"
            )

        return cls.__registered_softwares[software_id](*args, **kwargs)

    def get_context(self) -> SoftwareContext:
        """Get software's context"""

        return Context.get_software_context(
            software_id=self.get_id()
        )

    def get_drive(self) -> str:
        """Get drive"""

        return self.get_context().path.drive + '\\'

    def list_platforms(self) -> list[str]:
        """List platforms"""

        return list(self.get_context().platform_associations.keys())

    def retrieve_platform_roms_folder(
        self,
        platform: str
    ):
        """Retrieve platform's roms folder if exists"""

        return self.get_context().platform_associations.get(platform, '')

    def retrieve_media(self, resource: str) -> Media:
        """Retrieve the media for the specified resource"""

        for key, value in self.get_context().media_associations.items():
            if value == resource:
                return key
        return None

    def retrieve_retrobox_manager_game_info_software_id(
        self,
        platform: str,
        game_item: dict
    ) -> SoftwareId:
        """Retrieve the SoftwareId containing game info in the Retrobox Manager

        Priority:
        1. Source
        2. Current software

        Returns:
            SoftwareId or None if no game info cannot be found in the Retrobox Manager."""

        # Retrieve the source SoftwareId
        source_software_id = self.get_context().sources.get(
            Constants.SETUP_SOURCE_GAME_INFO,
            self.get_id()
        )
        if source_software_id == self.get_id():
            game_info_software = self
        else:
            game_info_software = self.get_registered_software(
                software_id=source_software_id
            )

        # Try to retrieve the Retrobox Manager game info from the source software
        if FileHelper.is_file_exists(
            game_info_software.retrieve_retrobox_manager_game_info_path(
                platform=platform,
                game_item=game_item
            )
        ):
            return source_software_id

        # Try to retrieve the Retrobox Manager game info from the current software
        if source_software_id != self.get_id():
            if FileHelper.is_file_exists(
                self.retrieve_retrobox_manager_game_info_path(
                    platform=platform,
                    game_item=game_item
                )
            ):
                return self.get_id()

        # Nothing found
        return self.get_id()

    def retrieve_retrobox_manager_game_info_path(
        self,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve Retrobox Manager game's info path"""

        game_info_path = os.path.join(
            Context.get_games_path(),
            platform,
            game_item[Constants.UI_TABLE_KEY_COL_ID],
            f'{self.get_id().value}{Constants.XML_EXTENSION}'
        )

        if FileHelper.is_file_exists(game_info_path):
            return game_info_path

        return None

    @abstractmethod
    def get_id(self) -> SoftwareId:
        """Get id"""

    @abstractmethod
    def list_roms_folders(self) -> list[str]:
        """List folders where a rom can be found"""

    @abstractmethod
    def get_default_platform_associations(self) -> dict[str, str]:
        """Get default platform associations"""

    @abstractmethod
    def get_default_media_associations(self) -> dict[Media, str]:
        """Get default media associations"""

    def get_default_media_positions(self) -> dict[tuple[int, int], Media]:
        """Get default media positions"""

    def list_media_resources(self) -> list[str]:
        """List media resources"""

    @abstractmethod
    def list_games_with_rom(self, platform: str) -> dict[str, str]:
        """List games in a dictionary where the key is the rom and the value is the name"""

    @abstractmethod
    def retrieve_media_files(self, platform: str, game_item: dict) -> dict[Media, str]:
        """Retrieve media files"""

    @abstractmethod
    def retrieve_rom_file(self, platform: str, game_item: dict) -> str:
        """Retrieve rom file"""

    @abstractmethod
    def retrieve_software_game_info_path(
        self,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve Software game's info path"""

    @abstractmethod
    def retrieve_game_info(
        self,
        game_info_path: str,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve game info"""

    @abstractmethod
    def retrieve_game_name(
        self,
        game_info_path: str,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve game's name"""

    @abstractmethod
    def retrieve_game_description(
        self,
        game_info_path: str,
        platform: str,
        game_item: dict
    ) -> str:
        """Retrieve game's description"""

    @abstractmethod
    def uninstall_game(
        self,
        platform: str,
        game_item: dict
    ) -> bool:
        """Uninstall game"""

    @abstractmethod
    def install_game(
        self,
        platform: str,
        game_item: dict,
        media_files: dict[Media, str],
        rom_file: str
    ) -> bool:
        """Install game with the specified media files, game info files and rom file"""
