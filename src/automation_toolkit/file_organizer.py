"""
File organizer module.

Scans a directory and moves files into subfolders based on their extension.
For example:
- *.jpg, *.png -> images/
- *.pdf, *.docx -> documents/
- *.mp3, *.wav -> audio/

Author: Harsh Kumar
"""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict


logger = logging.getLogger(__name__)


@dataclass
class FileOrganizerConfig:
    """Configuration for file organization rules."""
    extension_map: Dict[str, str] = field(default_factory=lambda: {
        ".jpg": "images",
        ".jpeg": "images",
        ".png": "images",
        ".gif": "images",
        ".pdf": "documents",
        ".docx": "documents",
        ".doc": "documents",
        ".txt": "documents",
        ".mp3": "audio",
        ".wav": "audio",
        ".mp4": "video",
        ".mkv": "video",
        ".csv": "data",
        ".xlsx": "data",
    })
    other_folder: str = "others"


class FileOrganizer:
    """
    Organizes files in a directory into folders based on file extensions.
    """

    def __init__(self, root_dir: str | Path, config: FileOrganizerConfig | None = None) -> None:
        self.root_dir = Path(root_dir).expanduser().resolve()
        self.config = config or FileOrganizerConfig()

    def organize(self) -> None:
        """
        Perform organization of files in the root directory.

        Creates target subdirectories when needed.
        """
        if not self.root_dir.exists():
            raise FileNotFoundError(f"Root directory does not exist: {self.root_dir}")

        logger.info("Starting file organization in %s", self.root_dir)

        for path in self.root_dir.iterdir():
            # Skip directories themselves – we only move files
            if path.is_dir():
                logger.debug("Skipping directory: %s", path)
                continue

            target_dir = self._get_target_directory(path.suffix.lower())
            destination = self.root_dir / target_dir / path.name

            destination.parent.mkdir(parents=True, exist_ok=True)
            logger.debug("Moving %s -> %s", path, destination)
            shutil.move(str(path), str(destination))

        logger.info("File organization completed.")

    def _get_target_directory(self, extension: str) -> str:
        """
        Return folder name based on file extension.
        Unknown extensions go into `other_folder`.
        """
        return self.config.extension_map.get(extension, self.config.other_folder)
