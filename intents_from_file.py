import json
from argparse import ArgumentParser

from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from environs import Env


def create_intent(project_id, display_name, training_texts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for text in training_texts:
        phrase_part = dialogflow.Intent.TrainingPhrase.Part(text=text)

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[phrase_part])
        training_phrases.append(training_phrase)

    reply_text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=reply_text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )

    print(f'Intent created: {response.display_name}')


def create_intents_from_json(project_id, json_filepath):
    with open(json_filepath, 'r') as json_file:
        json_string = json_file.read()
        intents = json.loads(json_string)

    for name, description in intents.items():
        questions = description['questions']
        answers = [description['answer']]
        try:
            create_intent(project_id, name, questions, answers)
        except InvalidArgument as ex:
            print(
                f"Intent wasn't created due to error: {ex.message}"
            )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    project_id = env('DF_PROJECT_ID')

    parser = ArgumentParser(
        description='Reads and creates intents from JSON file.'
    )
    parser.add_argument(
        'filepath', 
        type=str,
        help='path to JSON file with intents'
    )
    args = parser.parse_args()
    
    create_intents_from_json(project_id, args.filepath)
