# coding: utf-8
import logging
import json
import os
import sys

from communication import get_updates
from logic import main

def application(environ, start_response):
	# update = json.loads(environ['wsgi.input'].read())
	# main(update)
	status = '200 OK'
	response_body = "\n".join("{}\t\t{}".format(k, v) for k, v in os.environ.iteritems())
	header = [("Content-Type", "text/plain"), ("Content-Length", len(response_body))]
	start_response(status, header)
	return [response_body]


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s (%(thread)s) %(levelname)s - %(message)s", stream=sys.stdout, level=logging.DEBUG)
    logging.info("Starting your bot")
    get_updates(main)