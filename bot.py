from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from dialog_flow import get_intent_from_text


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
    
    tg_bot_token = env('TG_API_KEY')
    dialogflow_project_id = env('DF_PROJECT_ID')

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['df_project_id'] = dialogflow_project_id

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_user))
    
    updater.start_polling()
    print('Bot started')
    updater.idle()
