from environs import Env
from google.cloud import dialogflow


def get_intent_from_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result


if __name__ == '__main__':
    env = Env()
    env.read_env()
    
    project_id = env('DF_PROJECT_ID')
    text = 'Хай'
    
    response = get_intent_from_text(project_id, '00_00_00', text, 'ru')
    print(response)
