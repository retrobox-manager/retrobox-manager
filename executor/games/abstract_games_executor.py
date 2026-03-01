#!/usr/bin/python3
"""Abstract Games Executor"""

from executor.abstract_executor import AbstractExecutor
from libraries.constants.constants import Category
from libraries.context.context import Context
from software.abstract_software import AbstractSoftware

# pylint: disable=too-many-branches


class AbstractGamesExecutor(AbstractExecutor):
    """Abstract Games Executor"""

    def __init__(
        self,
        sub_items_enabled: bool = False
    ):
        """Initialize executor"""

        super().__init__(
            sub_items_enabled=sub_items_enabled
        )

        # Retrieve software
        self._software = AbstractSoftware.get_registered_software(
            software_id=Context.get_selected_software()
        )

    def get_category(self) -> Category:
        """Get Category"""

        return Category.GAMES
