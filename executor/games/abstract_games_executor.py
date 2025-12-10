#!/usr/bin/python3
"""Abstract Games Executor"""

import os
import re
from tkinter import messagebox, simpledialog
from dialogs.selection.selection_dialog import SelectionDialog
from executor.abstract_executor import AbstractExecutor
from frontend.front_end_factory import FrontEndFactory
from libraries.constants.constants import Action, Category
from libraries.context.context import Context
from libraries.file.file_helper import FileHelper
from libraries.xml.xml_helper import XmlHelper

# pylint: disable=too-many-branches


class AbstractGamesExecutor(AbstractExecutor):
    """Abstract Games Executor"""

    __PATH_PLATFORMS_XML = os.path.join(
        Context.get_games_path(),
        'platforms.xml'
    )

    _TAG_PLATFORMS = 'platforms'
    _TAG_PLATFORM = 'platform'
    _TAG_NAME = 'name'

    _ROM_FOLDER_NAME = 'rom'
    _MEDIA_FOLDER_NAME = 'media'

    def __init__(
        self
    ):
        """Initialize executor"""

        super().__init__()

        # Retrieve front end
        self._front_end = FrontEndFactory.create(
            front_end=Context.get_selected_front_end()
        )

        # Set platform's data
        self._platform_data = None

    def get_category(self) -> Category:
        """Get Category"""

        return Category.GAMES

    def confirm_execution(self, parent: any) -> bool:
        """Confirm for execution"""

        if self.get_action() != Action.EXPORT:
            return True

        # List data for all platforms
        platforms_data = []
        if FileHelper.is_file_exists(
            file_path=self.__PATH_PLATFORMS_XML
        ):
            platforms_data = XmlHelper.list_tag_data(
                xml_file_path=self.__PATH_PLATFORMS_XML,
                tag=self._TAG_PLATFORM
            )

        # If platform found for the front end
        for platform_data in platforms_data:
            if self._front_end.get_id() not in platform_data:
                continue
            if platform_data[self._front_end.get_id()] != Context.get_selected_platform():
                continue
            self._platform_data = platform_data
            return True

        # List unaffected platforms names
        unaffected_platforms_names = []
        for platform_data in platforms_data:
            if self._front_end.get_id() not in platform_data:
                unaffected_platforms_names.append(
                    platform_data[self._TAG_NAME]
                )

        # Ask if new platform
        is_new_platform = True
        if len(unaffected_platforms_names) > 0:
            is_new_platform = messagebox.askyesno(
                title=Context.get_text('question'),
                message=Context.get_text('question_new_platform'),
                parent=parent.winfo_toplevel()
            )

        # Ask an entry for the new platform
        if is_new_platform:
            while True:
                new_platform = simpledialog.askstring(
                    Context.get_text('confirmation'),
                    Context.get_text(
                        'confirm_create_platform'
                    ),
                    parent=parent.winfo_toplevel()
                )
                if new_platform is None:
                    return False

                if re.fullmatch(r"[a-zA-Z0-9. ]+", new_platform):
                    break

            # Create the new platform
            self._platform_data = {
                self._TAG_NAME: new_platform,
                self._front_end.get_id(): Context.get_selected_platform()
            }
            platforms_data.append(self._platform_data)

            # Generate the XML from platforms data
            XmlHelper.create_xml_from_list(
                data=platforms_data,
                root_tag=self._TAG_PLATFORMS,
                item_tag=self._TAG_PLATFORM,
                xml_file_path=self.__PATH_PLATFORMS_XML
            )
            return True

        # Ask a selection for the existing platform
        existing_platform = SelectionDialog(
            title=Context.get_text('selection'),
            message=Context.get_text('selection_platform'),
            values=unaffected_platforms_names,
            parent=parent.winfo_toplevel()
        ).result

        # Update the existing platform
        for platform_data in platforms_data:
            if platform_data[self._TAG_NAME] == existing_platform:
                self._platform_data = platform_data
                self._platform_data[
                    self._front_end.get_id()
                ] = Context.get_selected_platform()

                # Generate the XML from platforms data
                XmlHelper.create_xml_from_list(
                    data=platforms_data,
                    root_tag=self._TAG_PLATFORMS,
                    item_tag=self._TAG_PLATFORM,
                    xml_file_path=self.__PATH_PLATFORMS_XML
                )
                return True

        return False
