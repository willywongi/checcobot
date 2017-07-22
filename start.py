# coding: utf-8
import logging
import sys

from communication import get_updates
from logic import main

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s (%(thread)s) %(levelname)s - %(message)s", stream=sys.stdout, level=logging.DEBUG)
    logging.info("Starting your bot")
    get_updates(main)