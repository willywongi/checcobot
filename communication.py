import json
import logging
import os
import socket
from thread import start_new_thread
import sys
import time
import urllib
import urllib2

TELEGRAM_ENDPOINT = "https://api.telegram.org/bot"


class Api(object):
	def __init__(self, apikey, endpoint=TELEGRAM_ENDPOINT):
		self.apikey = apikey
		self.endpoint = endpoint
		
	def get_updates(self, callback, timeout=60):
		''' Start polling for bot updates ad libitum. Calls the provided callback upon receiving new updates.
		'''
		''' Must be greater by one than the highest 
			among the identifiers of previously received updates.
		'''
		update_id = None
		while True:
			try:
				data = self.call_telegram("getUpdates", timeout=60, offset=update_id)
			except socket.timeout:
				logging.debug("Resetting request for long polling...")
				continue
			else:
				
				result = data.get('result')
				if result:
					# offset: max(update_id) + 1
					update_id = max(r['update_id'] for r in result) + 1

				if data['ok']:
					for message in data['result']:
						start_new_thread(callback, (message, self))
				else:
					logging.error("Bad response from Telegram: %s", data)
			finally:
				# give the server a little breath.
				time.sleep(0.5)

	def call_telegram(self, method, **kwargs):
		'''Invoke a method on the Telegram API.
			Passes any keyword argument as paramters of the Telegram API.
			eg.:
			>>> call_telegram("getMe")
			{u'ok': True, u'result': {u'username': u'samplebot', u'first_name': u'SampleBot', u'id': 123456789}}

		'''
		url = "{}{}/{}".format(self.endpoint, self.apikey, method)
		if kwargs:
			data = urllib.urlencode(kwargs)
		else:
			data = None
		req = urllib2.Request(url, data=data)
		try:
			logging.info("Calling %s...", method)
			logging.debug("%s?%s", method, data)
			handler = urllib2.urlopen(req, timeout=60)
		except urllib2.HTTPError as exc:
			logging.error("Telegram HTTPError %s, %s", exc.getcode(), exc.read())
			raise

		except Exception:
			raise

		else:
			return json.loads(handler.read())
