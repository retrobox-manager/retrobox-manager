#!/usr/bin/python3
"""UI Button Grid"""

import tkinter as tk
from typing import Callable, Iterable

from libraries.constants.constants import Constants

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


class UIButtonGrid(tk.Frame):
    """Widget displaying a grid of buttons"""

    def __init__(
        self,
        parent: tk.Widget,
        rows: int,
        columns: int,
        action: Callable[[tk.Button, int, int], None],
        cell_width: int = 100,
        cell_height: int = 100
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
        self.__components: dict[tuple[int, int], tk.Button] = {}
        self.__action = action

        # Build components grid
        for row in range(rows):
            for column in range(columns):
                button_frame = tk.Frame(
                    self,
                    width=cell_width,
                    height=cell_height
                )
                button_frame.grid(
                    row=row,
                    column=column,
                    padx=Constants.UI_PAD_SMALL,
                    pady=Constants.UI_PAD_SMALL
                )
                button_frame.grid_propagate(False)
                button_component = tk.Button(
                    button_frame,
                    text=' ',
                    command=lambda r=row, c=column: self.__on_button_click(
                        r, c)
                )
                button_component.place(x=0, y=0, relwidth=1, relheight=1)
                self.__components[(row, column)] = button_component

    def __on_button_click(self, row: int, column: int) -> None:
        """Internal click handler"""

        button = self.get_button(row, column)
        if button and self.__action:
            self.__action(self, row, column)

    @property
    def rows(self) -> int:
        """Get rows"""

        return self.__rows

    @property
    def columns(self) -> int:
        """Get columns"""

        return self.__columns

    def get_button(self, row: int, column: int) -> tk.Button | None:
        """Return the button at (row, column) or None if out of bounds."""

        return self.__components.get((row, column))

    def list_buttons(self) -> Iterable[tk.Button]:
        """Return all button components."""

        return self.__components.values()
