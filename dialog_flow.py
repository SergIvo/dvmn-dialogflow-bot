from environs import Env
from google.cloud import api_keys_v2


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


if __name__ == '__main__':
    env = Env()
    env.read_env()
    
    project_id = env('PROJECT_ID')
    
    key = get_df_api_key(project_id, 'zero')
