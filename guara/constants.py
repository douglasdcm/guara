# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from logging import Logger, getLogger
from os import getenv

LOGGER: Logger = getLogger(__name__)

GUARA_VERBOSE = getenv("GUARA_VERBOSE", "true").lower() == "true"
GUARA_DISABLE_LOGS = getenv("GUARA_DISABLE_LOGS", "false").lower() == "true"
GUARA_DRY_RUN = getenv("GUARA_DRY_RUN", "false").lower() == "true"


def convert_variable_to_integer(variable) -> int:
    env_var = getenv(variable, "0")
    try:
        result = int(env_var)
        if result < 0:
            raise ValueError
        return result

    except (ValueError, TypeError):
        if GUARA_VERBOSE:
            LOGGER.warning(
                f"Invalid {variable} value: '{env_var}'."
                " Expected a positive integer. Defaulting to 0."
            )
        return 0


GUARA_PACING_TIME = convert_variable_to_integer("GUARA_PACING_TIME")

GUARA_RETRIES_ON_FAILURE = convert_variable_to_integer("GUARA_RETRIES_ON_FAILURE")

SECRET_DEFAULT_VALUE = "********"
