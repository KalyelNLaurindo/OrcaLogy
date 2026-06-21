"""Application entry point and logging configuration.

Exposes the Typer 'app' object so Poetry's script binding
('orca = "orcalogy.main:app"') can locate and launch the CLI.
Also configures the production-grade rotating JSON file logging.
"""

import json
import logging
import logging.handlers
from pathlib import Path

from orcalogy.cli.commands import app

__all__ = ["app", "setup_logging"]


class JsonFormatter(logging.Formatter):
    """Custom formatter to output logs as structured JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the logging record as a JSON string with key metadata."""
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "line_number": record.lineno,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


def setup_logging(log_file_path: Path | None = None) -> None:
    """Configure a RotatingFileHandler that writes structured JSON logs.

    Default log location is ~/.config/orcalogy/logs/orca.log.
    Rotates at 10MB keeping 5 backup files.
    """
    if log_file_path is None:
        log_file_path = Path.home() / ".config" / "orcalogy" / "logs" / "orca.log"

    # Ensure log directory exists
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # 10MB per file, 5 backup files (standard senior production settings)
    max_bytes = 10 * 1024 * 1024
    backup_count = 5

    handler = logging.handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    
    # Avoid duplicate rotating handlers if setup_logging is called multiple times
    for h in list(root_logger.handlers):
        if isinstance(h, logging.handlers.RotatingFileHandler):
            root_logger.removeHandler(h)

    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
