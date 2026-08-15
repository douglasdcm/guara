# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

"""
The entry point of the package.  The main function is
responsible for initializing the logger and handling command
line arguments.
"""

from logging import INFO, Logger, basicConfig, disable, getLogger

from guara.constants import GUARA_DISABLE_LOGS

if GUARA_DISABLE_LOGS:
    disable(INFO)


basicConfig(
    level=INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)
LOGGER: Logger = getLogger("guara")
