from environs import Env
from google.cloud import api_keys_v2
from google.cloud import dialogflow


def get_df_api_key(project_id, suffix):
#    Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f'My first API key - {suffix}'

    # Initialize request and set arguments.
    request = api_keys_v2.CreateKeyRequest()
    request.parent = f'projects/{project_id}/locations/global'
    request.key = key

    # Make the request and wait for the operation to complete.
    response = client.create_key(request=request).result()

    print(f'Successfully created an API key: {response.name}')
    # For authenticating with the API key, use the value in "response.key_string".
    # To restrict the usage of this API key, use the value in "response.name".
    return response


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
