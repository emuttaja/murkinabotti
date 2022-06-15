#!/usr/bin/env python

""" A bot that will ask a telegram group at what time the eating should happen.
Will have extra functionality some day.

Elias Ahokas
"""

import logging, time, datetime, pytz, requests

from telegram import (
    Poll,
    Update,
)

from telegram.ext import (
    Updater,
    CommandHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

import lunch_fetcher as lunch

# define polling time
FIN = pytz.timezone("Europe/Helsinki")
POLLING_TIME = datetime.time(hour=8, minute=0, tzinfo=FIN)


# define answers for the poll.
TIMES = [
    "10.30",
    "11.00",
    "11.30",
    "12.00",
    "13.00",
    "13.30",
    "14.00",
    "En tuu"
]

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
schedule_logger = logging.getLogger("schedule")
schedule_logger.setLevel(level=logging.DEBUG)


# Define some command handlers

def start(update: Update, context: CallbackContext):
    """Send a start message when either user starts a conversation or /start
    command is used

    Parameters
    ----------
    update : Update
        Updater for tg bot
    context : CallbackContext
        Command context
    """
    update.message.reply_text(
        "Hewwo :3 Mainly for use in the Tivoli -tg group.. @elijjjas is my creator. Message him if you want something"
    )



def murkina_poll(context: CallbackContext):
    """Sends a poll to a group when called

    Parameters
    ----------
    context : CallbackContext
        Context for the bot
    """
    context.bot.send_poll(
        "-1001403306654",
        "Mihin aikaan murkinaa?",
        TIMES,
        is_anonymous=False,
        allows_multiple_answers=True,
    )

def github(update: Update, context: CallbackContext):
    """Return a link to the github repository of this project when 
    /github command is given

    Args:
        update (Update): updater for tg bot
        context (CallbackContext): The callback context
    """
    update.message.reply_text(
        "Here you go uwu: https://github.com/emuttaja/murkinabotti"
    )

def send_cat(update: Update, context:CallbackContext):
    """Gets an ai generated picture of a cat from 
    https://thiscatdoesnotexist.com/ and sends it as a reply

    Parameters
    ----------
    update : Update
        Updater
    context : CallbackContext
        Context
    """
    #download the cat
    url = "https://thiscatdoesnotexist.com/"
    img_data = requests.get(url).content
    with open("cat.jpeg", "wb") as handler:
        handler.write(img_data)

    #send the cat
    photo = open("cat.jpeg", "rb")
    context.bot.send_photo(chat_id=update.effective_chat.id, 
                      photo=photo)
    photo.close()

def lunch_list(update: Updater, context:CallbackContext):
    """ Makes a message which has todays lunch list.

    Parameters
    ----------
    update : Updater
        bot updater
    context : CallbackContext
        bot context
    """
    lunch_list = lunch.get_lists()
    restaurants = lunch_list.keys()
    
    # format message
    final_message = ""
    for restaurant in restaurants:
        neat_list = ""
        for ingredient in lunch_list[restaurant]:
            neat_list += ingredient + "\n"
        message = f"{restaurant}: \n {neat_list} \n"

        final_message += message
        
    update.message.reply_text(
        final_message
    )

def main():
    # load up the api key
    file = open("api_key.txt", "r")
    api_key = file.readline()
    file.close()
    updater = Updater(api_key)
    dispatcher = updater.dispatcher

    # add handlers to updater
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("github", github))
    dispatcher.add_handler(CommandHandler("katti", send_cat))
    dispatcher.add_handler(CommandHandler("murkina", lunch_list))
    
    # start the job that starts the poll daily but only on weekdays
    job = updater.job_queue
    murkina_job = job.run_daily(murkina_poll, POLLING_TIME, days=(0,1,2,3,4))
    
    # Start the bot and run until ^C or sigterm
    updater.start_polling()
    updater.idle()



if __name__ == "__main__":
    main()
