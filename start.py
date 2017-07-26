# coding: utf-8
import logging
import os
import sys

from communication import Api
from logic import main


def long_poll(apikey, callback):
	''' When started from command line, a long polling, repeat-forever loop is started:
		1. a request is started and whenever:
		2. if the request times out: goto 1. (it's restarted)
		3. if Telegram sends a response (someone interacted w/ bot) a function is invoked in a thread and then goto 1.
	'''
	api = Api(apikey)
	api.get_updates(callback)


if __name__ == "__main__":
	logging.basicConfig(format="%(asctime)s (%(thread)s) %(levelname)s - %(message)s", stream=sys.stdout, level=logging.DEBUG)
	logging.info("Starting your bot")
	try:
		apikey = sys.argv[1]
	except IndexError:
		apikey = os.environ['TELEGRAM_APIKEY']

	long_poll(apikey, main)