# #################
token="5755974499:AAGS24gQXFg0UyjPjXqlfIUFN-ZqB5E0ucs"
# #################

# from time import sleep
# from telegram.ext.updater import Updater
# from telegram.update import Update
# # from telegram.ext import ContextTypes
# from telegram.ext import Application, CommandHandler, ContextTypes
# from telegram.ext.callbackcontext import CallbackContext
# # from telegram.ext.commandhandler import CommandHandler
# from telegram.ext.callbackqueryhandler import CallbackQueryHandler
# from telegram.ext.messagehandler import MessageHandler
# from telegram.ext.filters import Filters
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
  

# NotifierDict={}
  
# def start(update: Update, context: CallbackContext):
#     update.message.reply_text(
#         f"Hello {update.effective_user['first_name']}, Welcome to the Bot.Please write\
#         /help to see the commands available.")
  
# def help(update: Update, context: CallbackContext):
#     update.message.reply_text("""Available Commands :
#     /notifier -manage notifications""")

# def notifier(update: Update, context: CallbackContext):
#     update.message.reply_text("Choose action:",reply_markup=InlineKeyboardMarkup(
#         # [InlineKeyboardButton("A",callback_data="a") 
#         # # for q in ["List","Add","Delete","Modify"]
#         # ]
#         [[
#         InlineKeyboardButton("Option 1", callback_data='1'),
#         InlineKeyboardButton("Option 2", callback_data='2')
#     , InlineKeyboardButton("Option 3", callback_data='3')]]
#     )
# )
# async def button(update: Update, context):
#     query: CallbackQuery = update.callback_query
#     query.answer()
#     print(query.data)
#     sleep(10)
#     query.message.reply_text(text="Selected option: {query.data}")
#     # if update.id in NotifierDict.keys():
#     #     nots=NotifierDict[update.id]
#     #     update.message.reply_text(
#     #         "Your notifiers\n",
#     #         "\n".join([f"{q}:{q[0]} at {q[1]}" for q in len(nots)]) 
#     #         )
#     # else:update.message.reply_text("Nothing to show ._.")
# def unknown(update: Update, context: CallbackContext):update.message.reply_text(f"Sorry {update.message.text} is not a valid command")
  
  
# def unknown_text(update: Update, context: CallbackContext):update.message.reply_text("Sorry I can't recognize you , you said update.message.text")
  

# def main() -> None:

#     updater = Application.builder().token(token).build()
#     updater.dispatcher.add_handler(CommandHandler('start', start))
#     updater.dispatcher.add_handler(CommandHandler('help', help))
#     updater.dispatcher.add_handler(CommandHandler('notifier', notifier))
#     # updater.dispatcher.add_handler(CommandHandler('notifier add', notifierAdd))
#     # updater.dispatcher.add_handler(CommandHandler('notifier del', notifierDel))

#     updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
#     updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
#     updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

#     updater.dispatcher.add_handler(CallbackQueryHandler(button))
    
#     updater.run_polling()
# if __name__ == "__main__":
#     main()
#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.

This Bot uses the Application class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

#export PYTHONPATH="/home/dkfl/Prog/Python"

# import logging

# # from telegram import __version__ as TG_VER

# # try:
# #     from telegram import __version_info__
# # except ImportError:
# #     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )
# from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )


# Define a few command handlers. These usually take the two arguments update and
# context.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set <seconds> to set a timer")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
