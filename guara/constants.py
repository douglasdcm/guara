# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from logging import Logger, getLogger
from os import getenv

from guara.utils import convert_variable_to_integer

LOGGER: Logger = getLogger(__name__)

VERSION = "0.0.26rc1"
GUARA_VERBOSE = getenv("GUARA_VERBOSE", "true").lower() == "true"
GUARA_DISABLE_LOGS = getenv("GUARA_DISABLE_LOGS", "false").lower() == "true"
GUARA_DRY_RUN = getenv("GUARA_DRY_RUN", "false").lower() == "true"
GUARA_PACING_TIME = convert_variable_to_integer("GUARA_PACING_TIME", GUARA_VERBOSE)
GUARA_RETRIES_ON_FAILURE = convert_variable_to_integer(
    "GUARA_RETRIES_ON_FAILURE", GUARA_VERBOSE
)
SECRET_DEFAULT_VALUE = "********"
