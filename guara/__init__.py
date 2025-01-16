from logging import basicConfig, getLogger, Logger, INFO


basicConfig(
    level=INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)
LOGGER: Logger = getLogger("guara")
