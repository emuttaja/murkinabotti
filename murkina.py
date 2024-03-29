#!/usr/bin/env python

""" A bot that will ask a telegram group at what time the eating should happen.
Will have extra functionality some day.

"""

import logging, time, datetime, pytz, requests

from telegram import (
    Poll,
    Update,
    constants,
    ParseMode
)

from telegram.ext import (
    Updater,
    CommandHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    MessageFilter
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
    "12.30",
    "13.00",
    "13.30",
    "14.00",
    "EOS",
    "En tuu",
]

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
schedule_logger = logging.getLogger("schedule")
schedule_logger.setLevel(level=logging.DEBUG)



# define filters

class AutoCorrectFilter(MessageFilter):
    def wrong_letter_count(self, word, correct_word, case_sensitive=False):
        """counts how many of the letters are incorrect in arg 'word' compared to
        arg 'correct_word'. Can be case sensitive

        Parameters
        ----------
        word : str
            word to be compared
        correct_word : str
            the correct word
        case_sensitive : bool, optional
            The function can be case sensitive but, by default False

        Returns
        -------
        int
            how many of the letters were wrong. -1 if word and correct_word are
            not the same length
        """
        if len(word) != len(correct_word):
            return -1

        wrong_letters = 0
        for i in range(len(word)):
            letter = word[i]
            correct_letter = correct_word[i]
            if letter != correct_letter:
                if case_sensitive:
                    wrong_letters += 1
                    continue
                elif letter.swapcase() != correct_letter:
                    wrong_letters += 1    
        return wrong_letters

    def filter(self, message):
        """The main method the bot calls.

        Parameters
        ----------
        message : str, 
            message text

        Returns
        -------
        bool
            True if filtering passes, otherwise False
        """

        
        message_string = str(message.text)
        # bad handling of "äsh"

        if not len(message_string) == 3:
            return False
        if message_string == "äsu" or message_string == "Äsu":
            return False
        wrong_letter_count = self.wrong_letter_count(message_string, "äsh")        
        if wrong_letter_count == 1:
            return True


class eemeliFilter(MessageFilter):
    def filter(self, message):
        message_string = str(message.text)

        if message_string == "Oho!":
            return True





# Define command handlers

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
        "H-hewwo :3c"
    )

    update.message.reply_text(
        "Im mainly used in the Tivoli tg group.. @elijjjas is my creator. Message him if you need something."
    )

    update.message.reply_text(
        "To see all the things I support, please visit https://github.com/emuttaja/murkinabotti"
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

    #send the cat
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_data)

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
        message = f"<b>{restaurant}:</b>\n{neat_list}\n"

        final_message += message
        
    update.message.reply_text(
        final_message, 
        parse_mode = ParseMode.HTML
    )

def autocorrect_message(update: Updater, context: CallbackContext):
    update.message.reply_text(
        "Äsh*"
    )

def wabu(update: Updater, context: CallbackContext):
    """Reply the time to wappu

    Parameters
    ----------
    update : Updater
        updater
    context : CallbackContext
        context
    """
    now = datetime.datetime.now(tz=FIN)
    wabu = datetime.datetime(2023, 5, 1, 0, 0, tzinfo=FIN)
    time_to_wabu = wabu - now - datetime.timedelta(seconds=87600) # -1h20min for some reason -,-

    days, hours, minutes = time_to_wabu.days, time_to_wabu.seconds // 3600, time_to_wabu.seconds // 60 % 60
    seconds = time_to_wabu.seconds - hours*3600 - minutes*60

    message = (f"Wabuun on {days} päivää, "
               f"{hours} tuntia, "         
               f"{minutes} minuuttia ja "
               f"{seconds} sekuntia.")
    update.message.reply_text(
        message
    )

def wabuu(update: Updater, context: CallbackContext):
    photo = open("wabuu.jpg", "rb")
    context.bot.send_photo(chat_id=update.effective_chat.id, 
                      photo=photo)
    photo.close()

def commands(update: Updater, context: CallbackContext):
    message = (
        "Tuen seuraavia komentoja:\n"
        "/katti\n/murkina\n/wabu\n/github"
    )
    update.message.reply_text(
        message
    )

def sano_eemeli(update: Updater, context: CallbackContext):
    update.message.reply_text(
        "sano Eemeli"
    )



def main():
    # init a filter class
    autocorrect_filter = AutoCorrectFilter()
    eemeli_filter = eemeliFilter()

    # load up the api key
    file = open("api_key.txt", "r")
    api_key = file.readline()
    file.close()

    updater = Updater(api_key)
    dispatcher = updater.dispatcher

    # add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("github", github))
    dispatcher.add_handler(CommandHandler("katti", send_cat))
    dispatcher.add_handler(CommandHandler("murkina", lunch_list))
    dispatcher.add_handler(CommandHandler("wabu", wabu))
    dispatcher.add_handler(CommandHandler("1337", commands))
    dispatcher.add_handler(CommandHandler("wabuu", wabuu))

    dispatcher.add_handler(MessageHandler(autocorrect_filter, autocorrect_message))
    dispatcher.add_handler(MessageHandler(eemeli_filter, sano_eemeli))
    
    # start the job that starts the poll daily but only on weekdays
    job = updater.job_queue
    murkina_job = job.run_daily(murkina_poll, POLLING_TIME, days=(0,1,2,3,4))
    
    # Start the bot and run until ^C or sigterm
    updater.start_polling()
    updater.idle()



if __name__ == "__main__":
    main()
