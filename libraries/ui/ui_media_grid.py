#!/usr/bin/python3
"""UI Media Grid"""

import tkinter as tk
from typing import Iterable

from libraries.constants.constants import Constants
from libraries.ui.ui_media import UIMedia

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


class UIMediaGrid(tk.Frame):
    """Widget displaying a grid of UIMedia components"""

    def __init__(
        self,
        parent: tk.Widget,
        rows: int,
        columns: int,
        cell_width: int = 100,
        cell_height: int = 100,
        read_only: bool = False
    ):
        """Initialize UI"""

        super().__init__(
            parent
        )

        # Check rows and columns
        if rows <= 1 or columns <= 1:
            raise ValueError('Rows and columns must be at least 1!')

        # Initialize class variables
        self.__rows = rows
        self.__columns = columns
        self.__components: dict[tuple[int, int], UIMedia] = {}

        # Build components grid
        for row in range(rows):
            for column in range(columns):
                media_component = UIMedia(
                    parent=self,
                    width=cell_width,
                    height=cell_height,
                    read_only=read_only
                )
                media_component.grid(
                    row=row,
                    column=column,
                    padx=Constants.UI_PAD_SMALL,
                    pady=Constants.UI_PAD_SMALL
                )
                self.__components[(row, column)] = media_component

    @property
    def rows(self) -> int:
        """Get rows"""

        return self.__rows

    @property
    def columns(self) -> int:
        """Get columns"""

        return self.__columns

    def get_media(self, row: int, column: int) -> UIMedia | None:
        """Return the media at (row, column) or None if out of bounds."""

        return self.__components.get((row, column))

    def list_media(self) -> Iterable[UIMedia]:
        """Return all media components."""

        return self.__components.values()
