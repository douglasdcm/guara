from os import getenv

GUARA_DISABLE_LOGS = getenv("GUARA_DISABLE_LOGS", "false").lower() == "true"
GUARA_DRY_RUN = getenv("GUARA_DRY_RUN", "false").lower() == "true"
GUARA_PACING_TIME = int(getenv("GUARA_PACING_TIME", 0))
GUARA_RETRIES_ON_FAILURE = int(getenv("GUARA_RETRIES_ON_FAILURE", 0))
GUARA_VERBOSE = getenv("GUARA_VERBOSE", "true").lower() == "true"

SECRET_DEFAULT_VALUE = "<hidden>"
