# #################
token="5755974499:AAGS24gQXFg0UyjPjXqlfIUFN-ZqB5E0ucs"
# #################

import telebot

bot=telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def pv(message):
    bot.send_message(message.chat.id,message.text)
bot.polling(none_stop=True)
