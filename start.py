# coding: utf-8
import logging
import json
import os
from socket import getfqdn
import sys

from communication import get_updates
from logic import main

def application(environ, start_response):
	postdata = environ['wsgi.input'].read()
	status = '200 OK'
	if postdata:
		update = json.loads(environ['wsgi.input'].read())
		main(update)
		response_body = status
	else:
		response_body = "Nothing to see here, move along.\n\n{}".format(getfqdn())
	header = [("Content-Type", "text/plain"), ("Content-Length", str(len(response_body)))]
	start_response(status, header)
	return [response_body]


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s (%(thread)s) %(levelname)s - %(message)s", stream=sys.stdout, level=logging.DEBUG)
    logging.info("Starting your bot")
    get_updates(main)