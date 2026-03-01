#!/usr/bin/python3
"""UI Media"""

import os
import threading
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import vlc

from dialogs.waiting.waiting_dialog import WaitingDialog
from libraries.context.context import Context
from libraries.constants.constants import Constants, Media
from libraries.file.file_helper import FileHelper

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-nested-blocks
# pylint: disable=attribute-defined-outside-init


class UIMedia(tk.LabelFrame):
    """Class for UI Media"""

    def __init__(
        self,
        parent: tk.Widget,
        width: int,
        height: int,
        read_only: bool = False
    ):
        """Initialize UI"""

        super().__init__(
            parent
        )

        self.__media = None
        self.__vlc_window = None
        self.__vlc_media_player = None
        self.__media_file = None
        self.__media_folder = None
        self.__read_only = read_only

        # Create frame to show media
        self.__media_frame = tk.Frame(self)
        self.__media_frame.pack(
            side=tk.TOP,
            padx=Constants.UI_PAD_SMALL,
            pady=Constants.UI_PAD_SMALL
        )
        self.__media_frame.config(width=width, height=height)

        # Initialize VLC
        self.__init_vlc_params = []
        self.__vlc_instance = vlc.Instance(*self.__init_vlc_params)

        # Build a media's player
        self.__media_player = self.__vlc_instance.media_player_new()

        # Define where the media will be played
        self.__media_frame.update_idletasks()
        self.__media_player.set_hwnd(self.__media_frame.winfo_id())

        # Bind clicks
        self.bind("<Button-3>", self.__show_context_menu)
        self.__media_frame.bind("<Button-3>", self.__show_context_menu)

    def __show_context_menu(self, event):
        """Show context menu"""

        # Build context menu
        context_menu = tk.Menu(self, tearoff=0)

        # Actions to open/explore media
        if self.__media_file is not None:
            file_extension = FileHelper.retrieve_file_extension(
                file_path=self.__media_file
            )
            if file_extension in Constants.VLC_SUPPORTED_EXTENSIONS:
                context_menu.add_command(
                    label=Context.get_text('media_action_open_vlc'),
                    command=self.__open_vlc_window
                )

            context_menu.add_command(
                label=Context.get_text(
                    'target_action_explore',
                    target=Context.get_text('target_folder')
                ),
                command=self.__explore_folder
            )
            context_menu.add_separator()

        # Actions to export/import/delete media
        if not self.__read_only:
            context_menu.add_command(
                label=Context.get_text(
                    'target_action_import',
                    target=Context.get_text('target_media')
                ),
                command=self.__import_media
            )

        if self.__media_file is not None:
            context_menu.add_command(
                label=Context.get_text(
                    'target_action_export',
                    target=Context.get_text('target_media')
                ),
                command=self.__export_media
            )

        if self.__media_file is not None and not self.__read_only:
            context_menu.add_command(
                label=Context.get_text(
                    'target_action_delete',
                    target=Context.get_text('target_media')
                ),
                command=self.__delete_media
            )

        # Show context menu in the mouse's position
        context_menu.post(event.x_root, event.y_root)

        # Don't execute any other action in the button
        return "break"

    def __open_vlc_window(self):
        """Open the current media in a VLC window"""

        # Close VLC window if already open
        self.__close_vlc_window()

        # Create a new tkinter window
        self.__vlc_window = tk.Toplevel(self)
        self.__vlc_window.title(Context.get_text('media_title'))
        self.__vlc_window.geometry("800x600")

        # Initialize a new media player for the window
        self.__vlc_media_player = self.__vlc_instance.media_player_new()

        # Attach the video to the handle of the new window
        self.__vlc_window.update_idletasks()
        self.__vlc_media_player.set_hwnd(self.__vlc_window.winfo_id())

        # Set the media currently playing
        current_media = self.__media_player.get_media()
        if current_media:
            self.__vlc_media_player.set_media(current_media)

            # Play the video in the new window
            self.__vlc_media_player.play()

        # Add an action to exit fullscreen mode
        self.__vlc_window.bind(
            '<Escape>', lambda event: self.__close_vlc_window()
        )

        # Handle the window's close button (top-right 'X')
        self.__vlc_window.protocol("WM_DELETE_WINDOW", self.__close_vlc_window)

        # Set focus to the new window
        self.__vlc_window.focus_set()  # Set focus to the new window

        # Bring the window to the top of the stack
        self.__vlc_window.lift()

    def __explore_folder(self):
        """Explore the current folder in Windows Explorer"""

        FileHelper.explore_folder(
            folder_path=self.__media_folder
        )

    def __close_vlc_window(self):
        """Close VLC window"""

        if self.__vlc_window is not None:
            self.__vlc_media_player.stop()
            self.__vlc_window.destroy()
            self.__vlc_window = None

    def __import_media(self):
        """Import media from a file"""

        self.__source_file_path = filedialog.askopenfilename(
            parent=self.winfo_toplevel()
        )
        if self.__source_file_path:
            # Retrieve extension
            _, file_extension = os.path.splitext(self.__source_file_path)

            # Do nothing if the file is not a media file
            if file_extension not in Constants.VLC_SUPPORTED_EXTENSIONS:
                messagebox.showwarning(
                    Context.get_text('warning'),
                    Context.get_text('warning_not_a_media_file'),
                    parent=self.winfo_toplevel()
                )
                return

            # Execute the import in a waiting dialog
            WaitingDialog(
                parent=self.winfo_toplevel(),
                process_name=Context.get_text('process_importation'),
                process_function=self.__run_import_media
            )

    def __run_import_media(self, should_interrupt):
        """Run import media from a file"""

        # pylint: disable=unused-argument

        # Retrieve extension
        _, file_extension = os.path.splitext(self.__source_file_path)

        # Delete current file path is exists
        if self.__media_file is not None:
            # Close VLC window if already open
            self.__close_vlc_window()

            # Stop the media
            self.__safe_stop_media_player()

            # Delete the current file
            FileHelper.delete_file(
                file_path=self.__media_file
            )

        # Set new media file
        if self.__media_file is not None:
            self.__media_file = os.path.join(
                self.__media_folder,
                FileHelper.retrieve_file_basename(
                    file_path=self.__media_file
                ) + file_extension
            )
        else:
            self.__media_file = os.path.join(
                self.__media_folder,
                self.__media.value + file_extension
            )

        # Copy new media file
        FileHelper.copy_file(
            source_file_path=self.__source_file_path,
            destination_file_path=self.__media_file
        )

        # Play new media file
        self.update_media(
            media=self.__media,
            media_title=self.__media_title,
            media_folder=self.__media_folder,
            media_file=self.__media_file
        )

    def __export_media(self):
        """Export media in a file"""

        if self.__media_file is None:
            return

        # Retrieve extension
        file_extension = FileHelper.retrieve_file_extension(
            file_path=self.__media_file
        )

        # Retrieve initial file name
        initial_file_name = self.__media.name.replace('/', '_').lower()
        initial_file_name += '_'
        initial_file_name += FileHelper.retrieve_file_basename(
            file_path=self.__media_file
        )
        initial_file_name += file_extension

        # Ask destination file's path
        self.__destination_file_path = filedialog.asksaveasfilename(
            parent=self.winfo_toplevel(),
            initialfile=initial_file_name,
            defaultextension=file_extension,
            filetypes=[
                (Context.get_text('media_type'), f'*{file_extension}')
            ]
        )
        if self.__destination_file_path:
            # Execute the import in a waiting dialog
            WaitingDialog(
                parent=self.winfo_toplevel(),
                process_name=Context.get_text('process_exportation'),
                process_function=self.__run_export_media
            )

    def __run_export_media(self, should_interrupt):
        """Run export media"""

        # pylint: disable=unused-argument

        FileHelper.copy_file(
            source_file_path=self.__media_file,
            destination_file_path=self.__destination_file_path
        )

    def __delete_media(self):
        """Delete media"""

        if self.__media_file is None:
            return

        if messagebox.askokcancel(
            Context.get_text('confirmation'),
            Context.get_text('confirm_delete_media'),
            parent=self.winfo_toplevel()
        ):

            # Execute the delete in a waiting dialog
            WaitingDialog(
                parent=self.winfo_toplevel(),
                process_name=Context.get_text('process_deletion'),
                process_function=self.__run_delete_media
            )

    def __run_delete_media(self, should_interrupt):
        """Run delete media"""

        # pylint: disable=unused-argument

        # Close VLC window if already open
        self.__close_vlc_window()

        # Stop the media
        self.__safe_stop_media_player()

        # Delete the current file
        FileHelper.delete_file(
            file_path=self.__media_file
        )

        # Update media
        self.update_media(
            media=self.__media,
            media_title=self.__media_title,
            media_folder=self.__media_folder,
            media_file=None
        )

    def __safe_play_media_player(self, media_path, timeout=1, wait_file_timeout=0.5):
        """Play media player safely, waiting for file to be ready if needed"""

        if not media_path or not os.path.exists(media_path):
            print(f"❌ Media not found: {media_path}")

        # Wait until the file is ready (size stable and > 0)
        start = time.time()
        last_size = -1
        while time.time() - start < wait_file_timeout:
            size = os.path.getsize(media_path)
            if size == last_size and size > 0:
                break
            last_size = size
            time.sleep(0.02)
        else:
            print(f"⚠️ File may not be fully ready: {media_path}")

        finished = threading.Event()

        def _play():
            try:
                self.__media_player.play()
            except Exception:
                pass
            finally:
                finished.set()

        t = threading.Thread(target=_play, daemon=True)
        t.start()

        if not finished.wait(timeout):
            print("⚠️ VLC play blocked")
            return False

        return True

    def __safe_stop_media_player(self, timeout=1):
        """Stop media player safely"""

        finished = threading.Event()

        def _stop():
            try:
                self.__media_player.stop()
            except Exception:
                pass
            finally:
                finished.set()

        t = threading.Thread(target=_stop, daemon=True)
        t.start()

        if not finished.wait(timeout):
            print("⚠️ VLC stop blocked")

    def stop_media(self):
        """Stop the media"""

        self.__safe_stop_media_player()
        self.__media_frame.destroy()
        self.__vlc_instance.release()

    def update_media(
        self,
        media: Media,
        media_title: str,
        media_folder: str,
        media_file: str
    ):
        """Update media"""

        self.__media = media
        self.__media_title = media_title
        self.__media_folder = media_folder
        self.__media_file = media_file

        # Reconfigure the component
        if media_title is not None:
            self.configure(
                text=media_title,
                bd=2,
                relief='groove'
            )
        else:
            self.configure(
                text=' ',
                bd=0,
                relief='flat'
            )

        # Close VLC window if already open
        self.__close_vlc_window()

        # Stop the media
        self.__safe_stop_media_player()

        # Do nothing if no media
        if media_file is None:
            return

        # Retrieve media to play
        media_to_play = None
        file_extension = FileHelper.retrieve_file_extension(
            file_path=media_file
        )
        if file_extension == Constants.PDF_EXTENSION:
            media_to_play = os.path.join(
                Context.get_base_path(),
                Constants.PATH_RESOURCES,
                'img',
                'pdf.png'
            )
        elif file_extension in Constants.VLC_SUPPORTED_EXTENSIONS:
            media_to_play = media_file

        # Play media if possible
        if media_to_play is not None:
            # Change media
            media = self.__vlc_instance.media_new(media_to_play)
            self.__media_player.set_media(media)

            # Play media
            self.__safe_play_media_player(
                media_path=media_to_play
            )
