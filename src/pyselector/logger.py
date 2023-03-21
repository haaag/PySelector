# logger.py

from __future__ import annotations

import logging

reset_color = "\33[0m"
FMT = "[{levelname:^7}] {name}: {message}"

FORMATS = {
    logging.DEBUG: FMT,
    logging.INFO: f"\33[36m{FMT}{reset_color}",
    logging.WARNING: f"\33[33m{FMT}\33[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: f"\33[1m\33[31m{FMT}\33[0m",
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
