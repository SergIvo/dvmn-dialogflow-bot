from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text('Здравствуйте!')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    
    tg_bot_token = env('TG_API_KEY')
    updater = Updater(tg_bot_token)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    updater.start_polling()
    print('Bot started')
    updater.idle()
