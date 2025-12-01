"""
Log analyzer module.

Reads application log files and computes simple metrics:
- total lines
- number of ERROR / WARNING / INFO entries
- most recent log timestamp (if present)

Author: Harsh Kumar
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)


LOG_LEVEL_PATTERN = re.compile(r"\b(INFO|WARNING|ERROR|DEBUG|CRITICAL)\b")


@dataclass
class LogStats:
    total_lines: int
    level_counts: Dict[str, int]
    error_lines: int


class LogAnalyzer:
    """
    Analyze log files for basic statistics.
    """

    def __init__(self, log_path: str | Path) -> None:
        self.log_path = Path(log_path).expanduser().resolve()

    def analyze(self) -> LogStats:
        """
        Analyze the log file and return aggregated statistics.
        """
        if not self.log_path.exists():
            raise FileNotFoundError(f"Log file does not exist: {self.log_path}")

        total_lines = 0
        level_counts: Dict[str, int] = {}
        error_lines = 0

        logger.info("Analyzing log file: %s", self.log_path)

        with self.log_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                total_lines += 1

                match = LOG_LEVEL_PATTERN.search(line)
                if match:
                    level = match.group(1)
                    level_counts[level] = level_counts.get(level, 0) + 1

                    if level == "ERROR":
                        error_lines += 1

        logger.info("Log analysis complete: %s", self.log_path)
        return LogStats(
            total_lines=total_lines,
            level_counts=level_counts,
            error_lines=error_lines,
        )
