
import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, InlineQueryHandler, CallbackQueryHandler)
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup

import word_creator, scraper, database_app

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token="TOKEN", use_context=True)
dp = updater.dispatcher


LETTERS, LENGTH, OPTIONS = range(3)

options = [['existing', 'new', 'length', 'letters']]

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="hello! start a new game if you are ready!")

def game_init(update, context):
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id,
    text="OK! send me the letters then:)")
    return LETTERS

def letters_get(update, context):
    bot = context.bot
    global letters
    letters = update.message.text.strip().split(' ')
    bot.send_message(chat_id=update.effective_chat.id,
    text="OK! length of the word now:)")
    return LENGTH

def lenght_get(update, context):
    bot = context.bot
    global target_length
    target_length = int(update.message.text.strip())
    bot.send_message(chat_id=update.effective_chat.id,
        text="OK! that's fine",
        reply_markup=ReplyKeyboardMarkup(options, one_time_keyboard=True))

    return OPTIONS

def new_game(update, context):
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id,
        text='OK! type that shit!',
        reply_markup=ReplyKeyboardRemove())
    if update.message.text == 'length':
        return LENGTH
    else:
        return LETTERS

def exist(update, context):
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id,
    text=f"OK! fetching words from database...")
    answers = database_app.searching(target_length, letters)
    for pm in answers:
        bot.send_message(
            chat_id=update.effective_chat.id, text=pm,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("correct", callback_data=pm)]]))
    return OPTIONS

def new(update, context):
    bot = context.bot
    answers = []
    bot.send_message(chat_id=update.effective_chat.id,
    text=f"OK! starting this shit with\n {letters}\n it can take a while!")
    word_list = word_creator.WordMaker(target_length, letters)
    scraper.Word_Check(word_list, answers)
    for pm in answers:
        bot.send_message(
            chat_id=update.effective_chat.id, text=pm,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("correct", callback_data=pm)]]))
    word_creator.WordDump(str(target_length), answers)
    return OPTIONS

def checking(update, context):
    query = update.callback_query
    query.answer(text='OK!')
    database_app.addrepeatation(query.data)

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('OK! FUCK OFF!')
    return ConversationHandler.END

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Sorry! I do not know what to do with this!")



start_handler = CommandHandler('start', start)
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('game_init', game_init)],
    states={
        LETTERS: [MessageHandler(Filters.text, callback=letters_get)],
        LENGTH: [MessageHandler(Filters.text, callback=lenght_get)],
        OPTIONS: [
            MessageHandler(Filters.regex('^existing$'), exist),
            MessageHandler(Filters.regex('^new$'), new),
            MessageHandler(Filters.regex('^(length|letters)$'), new_game)
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
button = CallbackQueryHandler(checking)
unknown_handler = MessageHandler(Filters.command, unknown)






dp.add_handler(start_handler)
dp.add_handler(conv_handler)
dp.add_handler(button)
dp.add_handler(unknown_handler)

updater.start_polling()