#!/usr/bin/python3
"""Abstract Games Executor"""

from executor.abstract_executor import AbstractExecutor
from libraries.constants.constants import Category
from libraries.context.context import Context
from manager.manager_factory import ManagerFactory

# pylint: disable=too-many-branches


class AbstractGamesExecutor(AbstractExecutor):
    """Abstract Games Executor"""

    _ROM_FOLDER_NAME = 'rom'
    _MEDIA_FOLDER_NAME = 'media'

    def __init__(
        self
    ):
        """Initialize executor"""

        super().__init__()

        # Retrieve software manager
        self._software_manager = ManagerFactory.create(
            software=Context.get_selected_software()
        )

    def get_category(self) -> Category:
        """Get Category"""

        return Category.GAMES
