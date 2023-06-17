import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from dialog_flow import get_intent_from_text
from telegram_logging import TgLogsHandler

logger = logging.getLogger('tg-dialogflow-bot')


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text('Здравствуйте!')


def reply_to_user(update: Update, context: CallbackContext) -> None:
    session_id = str(update.message.chat_id)
    df_project_id = context.bot_data.get('df_project_id')
    detected_intent = get_intent_from_text(
        df_project_id,
        session_id,
        update.message.text,
        'ru'
    )
    reply_message = detected_intent.fulfillment_text
    update.message.reply_text(reply_message)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    
    tg_api_token = env('TG_API_KEY')
    dialogflow_project_id = env('DF_PROJECT_ID')
    tg_log_chat_id = env('TG_LOG_CHAT_ID')

    handler = TgLogsHandler(tg_api_token, tg_log_chat_id)
    handler.setFormatter(
        logging.Formatter('%(process)d %(levelname)s %(message)s')
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    updater = Updater(tg_api_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['df_project_id'] = dialogflow_project_id

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_user))
    
    logger.info('Bot started')
    while True:
        try:
            updater.start_polling()
            updater.idle()
        except Exception as ex:
            logger.exception(ex)
