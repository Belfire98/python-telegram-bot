#!/usr/bin/env python

import logging
import os
import sys
from typing import Optional

try:
    import fcntl
except ImportError:
    fcntl = None


def get_logger(*args, **kwargs) -> logging.Logger:
    """
    Returns a logger object with an appropriate name.

    If the file name points to a utils module, the logger name will simply be `telegram(.ext)`.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        :class:`logging.Logger`: The logger.
    """
    class_name = kwargs.get("class_name")
    file_name = args[0]

    parts = file_name.split("_")
    if parts[1].startswith("utils") and class_name is None:
        name = parts[0].rstrip(".")
    else:
        name = f"{parts[0]}{class_name or parts[1].capitalize()}"

    logger = logging.getLogger(name)

    # Set up logging to a file
    log_file = kwargs.get("log_file")
    if log_file:
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                fmt="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            if fcntl:
                fd = file_handler.stream.fileno()
                fcntl.flock(fd, fcntl.LOCK_EX)

    return logger
