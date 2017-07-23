# coding: utf8
import json
import logging
import os
import urllib2

APIAI_ENDPOINT = "https://api.api.ai/v1"
APIAI_TOKEN = os.environ['APIAI_TOKEN']
APIAI_VERSION = "20170723"
APIAI_LANGUAGE = "it"

logger = logging.getLogger('checcobot.apiai')

def call_apiai(method, **kwargs):
    url = "{0}/{1}?v={2}".format(APIAI_ENDPOINT, method, APIAI_VERSION)
    headers = {
        'Content-Type': "application/json; charset=utf-8",
        "Authorization" : "Bearer {0}".format(APIAI_TOKEN)
    }
    if kwargs:
        data = json.dumps(kwargs)
    else:
        data = None
    req = urllib2.Request(url, data=data, headers=headers)
    try:
        logger.info("Calling %s...", method)
        logger.debug("%s?%s", url, data)
        handler = urllib2.urlopen(req, timeout=10)
    except urllib2.HTTPError as exc:
        logging.error("%s, %s", exc.getcode(), exc.read())
        raise

    except Exception:
        raise

    else:
        return json.loads(handler.read())
