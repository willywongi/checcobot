import logging.config
import json
import os

from communication import Api
from logic import main


def get_wsgiapp(callback):
	# configuring logging
	logging.config.dictConfig({
		'formatters': {
			'default': {
				'format': '%(asctime)s\t%(levelname)-8s\t%(name)s\t%(message)s',
				'datefmt': '%Y-%m-%d %H:%M:%S',
			},
		},
		'handlers': {
			'console': {
				'level': 'DEBUG',
				'class': 'logging.StreamHandler',
				'formatter': 'simple',
			},
		},
		'root': {
			'level': 'INFO',
			'handlers': ['console']
		}
	})

	api = Api(os.environ['TELEGRAM_APIKEY'])
	def a(environ, start_response):
		''' This is the standard entry-point for any wsgi compliant webapp.
			If Telegram sends a request (someone interacted w/ bot) a function is invoked.
		'''
		if environ['PATH_INFO'].endswith(api.apikey):
			postdata = environ['wsgi.input'].read()
			status = '200 OK'
			if postdata:
				# we have and actual update from Telegram
				update = json.loads(postdata)
				try:
					callback(update, api)
				except Exception:
					logger.exception("Error while calculating response to update %s", update)
					status = "500 Internal Server Error"
				response_body = status
			else:
				# just someone hitting the webserver
				response_body = "Nothing to see here, move along.\n\n{}".format(getfqdn())
		else:
			status = "404 Not Found"
			response_body = "Not Found"
		
		header = [("Content-Type", "text/plain"), ("Content-Length", str(len(response_body)))]
		start_response(status, header)
		return [response_body]
	return a

application = get_wsgiapp(main)