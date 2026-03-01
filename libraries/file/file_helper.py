#!/usr/bin/python3
"""File Helper"""

import os
import fnmatch
from pathlib import Path
import re
import shutil

from libraries.context.context import Context
from libraries.logging.logging_helper import LoggingHelper

# pylint: disable=too-many-public-methods


class FileHelper:
    """Class to help usage of File"""

    @staticmethod
    def is_folder_exists(
        folder_path: str
    ):
        """Check if a folder exists"""
        return os.path.isdir(folder_path)

    @staticmethod
    def delete_folder(
        folder_path: str
    ) -> bool:
        """Delete a folder"""
        if not FileHelper.is_folder_exists(
            folder_path=folder_path
        ):
            return False

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'delete_folder_simulation',
                    folder=str(folder_path)
                )
            )
            return True

        LoggingHelper.log_info(
            message=Context.get_text(
                'delete_folder_in_progress',
                folder=str(folder_path)
            )
        )
        shutil.rmtree(folder_path)

        return True

    @staticmethod
    def is_file_exists(
        file_path: str
    ) -> bool:
        """Check if a file exists"""
        if file_path is None:
            return False

        return os.path.isfile(file_path)

    @staticmethod
    def compare_files(
        file1_path: str,
        file2_path: str
    ) -> bool:
        """Copy a file from source to destination"""
        if not FileHelper.is_file_exists(
            file_path=file1_path
        ):
            return not FileHelper.is_file_exists(
                file_path=file2_path
            )
        if not FileHelper.is_file_exists(
            file_path=file2_path
        ):
            return False

        size_file1 = os.path.getsize(file1_path)
        size_file2 = os.path.getsize(file2_path)
        return size_file1 == size_file2

    @staticmethod
    def list_sub_directories(
        folder_path: str
    ) -> list[str]:
        """List sub directories for the specified folder"""
        if not FileHelper.is_folder_exists(
            folder_path=folder_path
        ):
            return []

        return os.listdir(folder_path)

    @staticmethod
    def list_relative_paths(
        folder_path: str,
        file_name: str,
        error_if_not_found=True
    ) -> list[str]:
        """List recursively relative paths for the specified name"""
        result = []
        if not os.path.isdir(folder_path):
            return []
        for root, dirs, files in os.walk(folder_path):
            # If a folder exists with the name of the file, add sub files
            if file_name in dirs:
                sub_folder_path = os.path.join(
                    root,
                    file_name
                )
                sub_files = FileHelper.list_relative_paths(
                    folder_path=sub_folder_path,
                    file_name='*',
                    error_if_not_found=False
                )
                for file_path in sub_files:
                    full_path = os.path.join(sub_folder_path, file_path)
                    relative_path = os.path.relpath(full_path, folder_path)
                    result.append(relative_path)
            # Try to find files
            for file_path in files:
                if file_path == file_name or \
                        FileHelper.retrieve_file_basename(file_path) == file_name or \
                        fnmatch.fnmatch(file_path, f'{file_name}.*'):
                    full_path = os.path.join(root, file_path)
                    relative_path = os.path.relpath(full_path, folder_path)
                    if file_path == 'Thumbs.db':
                        # Delete Thumbs.db
                        FileHelper.delete_file(
                            file_path=file_path
                        )
                        continue
                    result.append(relative_path)

        if error_if_not_found and len(result) == 0:
            raise Exception(Context.get_text(
                'error_missing_file',
                file=file_name,
                folder=str(folder_path)
            ))

        return result

    @staticmethod
    def copy_file(
        source_file_path: str,
        destination_file_path: str
    ) -> bool:
        """Copy a file from source to destination"""
        if os.path.exists(destination_file_path):
            if FileHelper.compare_files(source_file_path, destination_file_path):
                return False

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'copy_file_simulation',
                    source_file=str(source_file_path),
                    destination_file=str(destination_file_path)
                )
            )
            return True

        LoggingHelper.log_info(
            message=Context.get_text(
                'copy_file_in_progress',
                source_file=str(source_file_path),
                destination_file=str(destination_file_path)
            )
        )

        try:
            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
            shutil.copy2(source_file_path, destination_file_path)
        except Exception as exc:
            LoggingHelper.log_error(
                message=Context.get_text(
                    'error_copy_file',
                    source_file=str(source_file_path),
                    destination_file=str(destination_file_path)
                ),
                exc=exc
            )
            return False

        return True

    @staticmethod
    def move_file(
        source_file_path: str,
        destination_file_path: str
    ) -> bool:
        """Move a file from source to destination"""

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'move_file_simulation',
                    source_file=str(source_file_path),
                    destination_file=str(destination_file_path)
                )
            )
            return True

        LoggingHelper.log_info(
            message=Context.get_text(
                'move_file_in_progress',
                source_file=str(source_file_path),
                destination_file=str(destination_file_path)
            )
        )

        try:
            shutil.move(source_file_path, destination_file_path)
        except Exception as exc:
            LoggingHelper.log_error(
                message=Context.get_text(
                    'error_move_file',
                    source_file=str(source_file_path),
                    destination_file=str(destination_file_path)
                ),
                exc=exc
            )
            return False

        return True

    @staticmethod
    def copy_folder(
        source_folder_path: str,
        destination_folder_path: str
    ) -> bool:
        """Copy a folder from source to destination"""

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'copy_folder_simulation',
                    source_folder=str(source_folder_path),
                    destination_folder=str(destination_folder_path)
                )
            )
            return True

        LoggingHelper.log_info(
            message=Context.get_text(
                'copy_folder_in_progress',
                source_folder=str(source_folder_path),
                destination_folder=str(destination_folder_path)
            )
        )

        try:
            os.makedirs(os.path.dirname(
                destination_folder_path), exist_ok=True)
            shutil.copytree(source_folder_path, destination_folder_path)
        except Exception as exc:
            LoggingHelper.log_error(
                message=Context.get_text(
                    'error_copy_folder',
                    source_folder=str(source_folder_path),
                    destination_folder=str(destination_folder_path)
                ),
                exc=exc
            )
            return False

        return True

    @staticmethod
    def move_folder(
        source_folder_path: str,
        destination_folder_path: str
    ) -> bool:
        """Move a folder from source to destination"""

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'move_folder_simulation',
                    source_folder=str(source_folder_path),
                    destination_folder=str(destination_folder_path)
                )
            )
            return True

        LoggingHelper.log_info(
            message=Context.get_text(
                'move_folder_in_progress',
                source_folder=str(source_folder_path),
                destination_folder=str(destination_folder_path)
            )
        )

        try:
            shutil.move(source_folder_path, destination_folder_path)
        except Exception as exc:
            LoggingHelper.log_error(
                message=Context.get_text(
                    'error_move_folder',
                    source_folder=str(source_folder_path),
                    destination_folder=str(destination_folder_path)
                ),
                exc=exc
            )
            return False

        return True

    @staticmethod
    def create_folder(
        folder_path: str
    ):
        """Create a folder"""

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'create_folder_simulation',
                    folder=str(folder_path)
                )
            )
            return True

        LoggingHelper.log_info(
            message=Context.get_text(
                'create_folder_in_progress',
                folder=str(folder_path)
            )
        )

        os.makedirs(folder_path, exist_ok=True)

        return True

    @staticmethod
    def explore_folder(
        folder_path: str
    ):
        """Explore a folder"""

        os.makedirs(folder_path, exist_ok=True)
        os.startfile(folder_path)

    @staticmethod
    def retrieve_file_extension(
        file_path: str,
    ) -> str:
        """Retrieve the file's extension"""
        if file_path is None:
            return None

        path = Path(file_path)

        if len(path.suffixes) >= 2 and path.suffixes[-2:] == [".tar", ".gz"]:
            return ".tar.gz"

        return path.suffix

    @staticmethod
    def retrieve_file_basename(
        file_path: str,
    ) -> str:
        """Retrieve the file's basename (without extension)"""
        return Path(file_path).stem

    @staticmethod
    def retrieve_file_name(
        file_path: str,
    ) -> str:
        """Retrieve the file's name (with extension)"""
        return Path(file_path).name

    @staticmethod
    def retrieve_file_parent(
        file_path: str,
    ) -> str:
        """Retrieve the file's parent"""
        return Path(file_path).parent

    @staticmethod
    def retrieve_absolute_path(
        folder_path: str,
        relative_path: str
    ):
        """Retrieve the absolute path from a folder's path and a relative path"""
        return (Path(folder_path) / relative_path).resolve()

    @staticmethod
    def retrieve_relative_path(
        folder_path: str,
        file_path: str
    ):
        """Retrieve the relative path from a folder's path and an absolute path"""
        return str(Path(file_path).resolve().relative_to(Path(folder_path).resolve()))

    @staticmethod
    def delete_file(
        file_path: str,
        delete_all_extensions: bool = False
    ) -> bool:
        """Delete a file and eeventullay all its extensions"""
        if not FileHelper.is_file_exists(
            file_path=file_path
        ):
            return False

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'delete_file_simulation',
                    file=str(file_path)
                )
            )
            return True

        # If only 1 file to delete
        if not delete_all_extensions:
            LoggingHelper.log_info(
                message=Context.get_text(
                    'delete_file_in_progress',
                    file=str(file_path)
                )
            )

            os.remove(file_path)
            return True

        # Delete recursively files with the same basename
        deleted_files_count = 0
        parent_path = FileHelper.retrieve_file_parent(
            file_path=file_path
        )
        for relative_path in FileHelper.list_relative_paths(
            folder_path=parent_path,
            file_name=FileHelper.retrieve_file_basename(file_path),
            error_if_not_found=False
        ):
            if FileHelper.delete_file(
                file_path=os.path.join(
                    parent_path,
                    relative_path
                ),
                delete_all_extensions=False
            ):
                deleted_files_count += 1

        return deleted_files_count > 0

    @staticmethod
    def read_file(
        file_path: str,
        encoding='UTF-8'
    ) -> str:
        """Read a file"""
        if not FileHelper.is_file_exists(
            file_path=file_path
        ):
            return ''

        with open(
            file_path,
            mode='r',
            encoding=encoding
        ) as file:
            return file.read()

    @staticmethod
    def write_file(
        file_path: str,
        content: str,
        encoding='UTF-8'
    ):
        """Write content in a file"""

        if Context.is_simulated():
            LoggingHelper.log_info(
                message=Context.get_text(
                    'write_file_simulation',
                    file=str(file_path)
                )
            )
            return True

        LoggingHelper.log_info(
            message=Context.get_text(
                'write_file_in_progress',
                file=str(file_path)
            )
        )

        with open(
            file_path,
            mode='w',
            newline='\n',
            encoding=encoding
        ) as file:
            file.write(content)

        return True

    @staticmethod
    def get_included_files(file_path: str):
        """Returns the list of files referenced in a .cue or .m3u file"""

        included_files = []

        if file_path is None:
            return included_files

        extension = FileHelper.retrieve_file_extension(file_path=file_path)
        parent_dir = os.path.dirname(os.path.abspath(file_path))

        if extension not in (".cue", ".m3u"):
            return included_files

        with open(
                file_path,
                mode="r",
                encoding="utf-8",
                errors="ignore"
        ) as file:
            for line in file:
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # CUE file: FILE "filename.bin" BINARY
                if extension == '.cue':
                    match = re.match(r'FILE\s+"(.+?)"', line, re.IGNORECASE)
                    if match:
                        filename = match.group(1)
                        included_files.append(
                            os.path.join(parent_dir, filename)
                        )

                # M3U file: one file per line
                elif extension == '.m3u':
                    included_files.append(os.path.join(parent_dir, line))

        return included_files

    @staticmethod
    def get_main_file(files_paths: list[str]) -> str:
        """Returns the main file from a list of files"""

        # If no files
        if files_paths is None or len(files_paths) == 0:
            return None

        # If include some files (CUE file or M3U file)
        for file_path in files_paths:
            extension = FileHelper.retrieve_file_extension(file_path=file_path)
            if extension in ['.cue', '.m3u']:
                return file_path

        # Return the first file otherwise
        return files_paths[0]
