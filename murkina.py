#!/usr/bin/env python

""" A bot that will ask a telegram group at what time the eating should happen.
Will have extra functionality some day.

Elias Ahokas
"""
import logging, time, datetime, pytz

from telegram import (
    Poll,
    Update,
)

# from telegram.constants import ParseMode

from telegram.ext import (
    Updater,
    CommandHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

# define polling time
FIN = pytz.timezone("Europe/Helsinki")
POLLING_TIME = datetime.time(hour=8, minute=0, tzinfo=FIN)


# define answers for the poll.
TIMES = [
    "10.00",
    "10.30",
    "11.00",
    "11.30",
    "12.00",
    "12.30",
    "Pidä tunkkis"
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
    """Message something random when a user interacts with the bot for the
    first time to confuse them"""
    update.message.reply_text(
        "Hewwo :3 Mainly for use in the Tivoli -tg group.. @elijjjas is my creator. Message him if you want something"
    )



def murkina_poll(context: CallbackContext):
    """Send thö murkina poll"""
    # print("Toimis ny")
    context.bot.send_poll(
        "1962469908",
        "Mihin aikaan murkinaa?",
        TIMES,
        is_anonymous=False,
        allows_multiple_answers=True,
    )

def github(update: Update, context: CallbackContext):
    """Reply with the github repository of this project"""
    update.message.reply_text(
        "Here you go uwu: https://github.com/emuttaja/murkina-botti"
    )


def main():
    # load up the api key
    file = open("api_key.txt", "r")
    api_key = file.readline()
    updater = Updater(api_key)
    dispatcher = updater.dispatcher

    # add handlers to updater
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("github", github))
    
    # start the job that starts the poll daily but only on weekdays
    job = updater.job_queue
    murkina_job = job.run_daily(murkina_poll, POLLING_TIME, days=(0,1,2,3,4))
    
    # Start the bot and run until ^C or sigterm
    updater.start_polling()
    updater.idle()



if __name__ == "__main__":
    main()
