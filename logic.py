# coding: utf-8
import time

from communication import call_telegram

def main(update):
    chat_id = update['message']['chat']['id']
    call_telegram("sendChatAction", chat_id=chat_id, action="typing")
    time.sleep(2)
    call_telegram("sendMessage", chat_id=chat_id, text="Hi! I'm a bot.")
    