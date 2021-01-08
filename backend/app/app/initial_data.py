import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    pass


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
