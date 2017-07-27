# pybot-base
A skeleton for a Telegram based bot, written in Python 2.

## quick start
Provide a Telegram API key as an env variable (`TELEGRAM_APIKEY`) or as the command line argument:
```bash
$ export TELEGRAM_APIKEY = 123456:ABCDEFG0123456789
$ python start.py
```
```bash
$ python start.py 123456:ABCDEFG0123456789
```
When running, this bot will always answer "Hi! I'm a bot."
Please fork this repo and personalize how the bot will answer; just have a look at the Telegram API: https://core.telegram.org/bots/api.

## Long polling or webhook?
Your bot logic can get updates (ie. messages and other interactions with your bot) in two ways:
### Long polling
A forever-looping request is issued; Telegram batches the updates and send them over to respond to the request. After that, the request is re-issued.
See `start.py`.
### Webhook
You tell Telegram to send any update to a certain address. In order to have that you need an internet exposed web server with HTTPS support. See `wsgi.py`.

