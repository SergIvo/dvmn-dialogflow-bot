import random
import logging

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from dialog_flow import get_intent_from_text
from telegram_logging import TgLogsHandler

logger = logging.getLogger('vk-dialogflow-bot')


def reply_to_message(df_project_id, event, vk_api):
    session_id = str(event.user_id)
    detected_intent = get_intent_from_text(
        df_project_id,
        session_id,
        event.text,
        'ru'
    )
    if not detected_intent.intent.is_fallback:
        reply_message = detected_intent.fulfillment_text
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply_message,
            random_id=random.randint(1,1000)
        )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    vk_group_token = env('VK_GROUP_TOKEN')
    dialogflow_project_id = env('DF_PROJECT_ID')
    tg_log_chat_id = env('TG_LOG_CHAT_ID')
    tg_api_token = env('TG_API_KEY')

    handler = TgLogsHandler(tg_api_token, tg_log_chat_id)
    handler.setFormatter(
        logging.Formatter('%(process)d %(levelname)s %(message)s')
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info('Bot started')
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    reply_to_message(dialogflow_project_id, event, vk_api)
        except Exception as ex:
            logger.exception(ex)
