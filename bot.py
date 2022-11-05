#################

#################

from time import sleep
from telegram.ext.updater import Updater
from telegram.update import Update
# from telegram.ext import ContextTypes
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext.callbackcontext import CallbackContext
# from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
  

NotifierDict={}
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Hello {update.effective_user['first_name']}, Welcome to the Bot.Please write\
        /help to see the commands available.")
  
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :
    /notifier -manage notifications""")

def notifier(update: Update, context: CallbackContext):
    update.message.reply_text("Choose action:",reply_markup=InlineKeyboardMarkup(
        # [InlineKeyboardButton("A",callback_data="a") 
        # # for q in ["List","Add","Delete","Modify"]
        # ]
        [[
        InlineKeyboardButton("Option 1", callback_data='1'),
        InlineKeyboardButton("Option 2", callback_data='2')
    , InlineKeyboardButton("Option 3", callback_data='3')]]
    )
)
async def button(update: Update, context):
    query: CallbackQuery = update.callback_query
    query.answer()
    print(query.data)
    sleep(10)
    query.message.reply_text(text="Selected option: {query.data}")
    # if update.id in NotifierDict.keys():
    #     nots=NotifierDict[update.id]
    #     update.message.reply_text(
    #         "Your notifiers\n",
    #         "\n".join([f"{q}:{q[0]} at {q[1]}" for q in len(nots)]) 
    #         )
    # else:update.message.reply_text("Nothing to show ._.")
def unknown(update: Update, context: CallbackContext):update.message.reply_text(f"Sorry {update.message.text} is not a valid command")
  
  
def unknown_text(update: Update, context: CallbackContext):update.message.reply_text("Sorry I can't recognize you , you said update.message.text")
  

def main() -> None:

    updater = Application.builder().token(token).build()
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('notifier', notifier))
    # updater.dispatcher.add_handler(CommandHandler('notifier add', notifierAdd))
    # updater.dispatcher.add_handler(CommandHandler('notifier del', notifierDel))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.run_polling()
if __name__ == "__main__":
    main()