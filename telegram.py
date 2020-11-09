#!/usr/bin/python3

import json
import logging
from urllib import request, parse

import config
import utils

# import display
display_config = config.conf["atm"]["display"]
display = getattr(__import__("displays", fromlist=[display_config]), display_config)

logger = logging.getLogger("LNTXBOT")

class TelegramHandler(logging.StreamHandler):
    """Allow for logging to Telegram
    """
    def emit(self,record):
        
        self.send_message(record.getMessage())

    def send_message(self,message):
        """Send a message over Telegram
        """
        logger.info("Sending message [{}]".format(message))

        bot_key=config.conf["telegram"]["bot_key"] 
        user_id=config.conf["telegram"]["user_id"] 

        # Message object
        data = { 
            "chat_id": user_id,
            "text": message,
             }

        data = json.dumps(data)
        data = str(data)
        data = data.encode('utf-8')

        # Post Method is invoked if data != None
        req =  request.Request(
                "https://api.telegram.org/bot{bot_key}/sendMessage".format(bot_key=bot_key),
                data=data,
                headers={
                    "Content-Type":"application/json",
                    })

        # Response
        resp = request.urlopen(req)
