#!/usr/bin/python3
"""Manager Factory"""

from libraries.constants.constants import Software
from manager.abstract_manager import AbstractManager
from manager.batocera.batocera_manager import BatoceraManager
from manager.emu_movies.emu_movies_manager import EmuMoviesManager
from manager.launchbox.launchbox_manager import LaunchboxManager
from manager.skraper.skraper_manager import SkraperManager


class ManagerFactory:
    """Manager Factory"""

    @staticmethod
    def create(software: Software) -> AbstractManager:
        """Create Manager for the specified Software"""

        match(software):
            case Software.BATOCERA:
                return BatoceraManager()
            case Software.LAUNCHBOX:
                return LaunchboxManager()
            case Software.EMU_MOVIES:
                return EmuMoviesManager()
            case Software.SKRAPER:
                return SkraperManager()
            case _:
                raise Exception('Unimplemented Software!')
