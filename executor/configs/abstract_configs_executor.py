#!/usr/bin/python3
"""Abstract Configs Executor"""

from executor.abstract_executor import AbstractExecutor
from libraries.constants.constants import Category
from libraries.context.context import Context
from software.abstract_software import AbstractSoftware

# pylint: disable=too-many-branches


class AbstractConfigsExecutor(AbstractExecutor):
    """Abstract Configs Executor"""

    def __init__(
        self
    ):
        """Initialize executor"""

        super().__init__(
            sub_items_enabled=False
        )

        # Retrieve software manager
        self._software = AbstractSoftware.get_registered_software(
            software_id=Context.get_selected_software()
        )

    def get_category(self) -> Category:
        """Get Category"""

        return Category.CONFIGS

    def list_sub_items(self, item: dict) -> list[dict]:
        """List sub items for the current item"""

        return []
