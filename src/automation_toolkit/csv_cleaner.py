"""
CSV cleaner module.

Performs simple cleaning operations on CSV files:
- trims whitespace
- drops rows with all empty values
- optionally fills missing values with a default

Author: Harsh Kumar
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import pandas as pd  # type: ignore

logger = logging.getLogger(__name__)


@dataclass
class CSVCleanerConfig:
    fillna_value: Optional[Any] = None
    drop_empty_rows: bool = True
    strip_whitespace: bool = True


class CSVCleaner:
    """
    A simple CSV cleaner using pandas.
    """

    def __init__(self, input_path: str | Path, output_path: str | Path, config: CSVCleanerConfig | None = None) -> None:
        self.input_path = Path(input_path).expanduser().resolve()
        self.output_path = Path(output_path).expanduser().resolve()
        self.config = config or CSVCleanerConfig()

    def clean(self) -> None:
        """
        Load, clean, and write a new CSV file.
        """
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input CSV does not exist: {self.input_path}")

        logger.info("Reading CSV: %s", self.input_path)
        df = pd.read_csv(self.input_path)

        if self.config.strip_whitespace:
            logger.debug("Stripping whitespace from string columns.")
            for col in df.select_dtypes(include="object").columns:
                df[col] = df[col].astype(str).str.strip()

        if self.config.drop_empty_rows:
            before = len(df)
            df = df.dropna(how="all")
            after = len(df)
            logger.debug("Dropped %d empty rows.", before - after)

        if self.config.fillna_value is not None:
            logger.debug("Filling missing values with %r", self.config.fillna_value)
            df = df.fillna(self.config.fillna_value)

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Writing cleaned CSV: %s", self.output_path)
        df.to_csv(self.output_path, index=False)
