# coding: utf-8
import time

def main(update, api):
	chat_id = update['message']['chat']['id']
	api.call_telegram("sendChatAction", chat_id=chat_id, action="typing")
	time.sleep(2)
	api.call_telegram("sendMessage", chat_id=chat_id, text="Hi! I'm a bot.")
