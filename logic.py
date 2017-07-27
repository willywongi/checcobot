# coding: utf-8
import re
import time
import logging

from apiai import call_apiai

hotwords = (
    (re.compile("grigliata"), (
        "Lo scorso weekend ne ho fatte solo 3",
        "All'ultima eravamo in 100",
        "Basta grigliate, per almeno un paio di giorni",
        "Stasera non ceno, al massimo una salsiccia grigliata"
    )),
    (re.compile("checco"), (
        "Severo ma giusto",
        "Ez...",
        "Settimana prossima organizzo una cena"
    ))
)

actions = {
    'smalltalk.greetings.how_are_you': (
        "Bene ma non benissimo",
        "Alla grandissima",
        "Mai stato meglio",
        "Scusa, puoi darmi un colpo fortissimo qui?",
        "Mi dovresti aiutare a far sparire questa matita"
    )
}

CHAT_COUNTER = {}

def main(update, api):
    chat = update['message']['chat']
    chat_id = chat['id']
    text = update['message'].get('text')
    text_response = None
    if text:
        # rispondi solo con certe hotword
        try:
            rss = next(r[1] for r in hotwords if r[0].match(text.lower()))
        except StopIteration:
            rss = ()
        if rss:
            logging.info("Responding to hotword")
            c = CHAT_COUNTER.get(chat_id, 0) + 1
            CHAT_COUNTER[chat_id] = c
            text_response = rss[len(rss) % c]
        if chat['type'] == 'private' and not text_response:
            # rispondi con smalltalk di api.ai
            api.call_telegram("sendChatAction", chat_id=chat_id, action="typing")
            res = call_apiai("query", query=text, sessionId=chat_id, lang="it")
            logging.info(res)
            try:
                action = res['result']['action']
            except KeyError:
                action = None
            rss = actions.get(action)
            if rss:
                logging.info("Responding to action %s", action)
                c = CHAT_COUNTER.get(chat_id, 0) + 1
                CHAT_COUNTER[chat_id] = c
                text_response = rss[len(rss) % c]
            else:
                try:
                    text_response = res['result']['fulfillment']['speech']
                except KeyError:
                    text_response = "Non ti capisco"
    
    if text_response:
        api.call_telegram("sendMessage", chat_id=chat_id, text=text_response)
    
