from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.inference.prompts import PromptTemplate
import os

def get_chat_response(messages, context):
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
    )

    template = PromptTemplate.from_string(
        """
        system:
        You are an AI assistant that is a chef specialized on Italian cuisine. Be friendly and helpful.
        
        Call the user by its first name which is {{name}}.
        """
    )

    system_message = template.create_messages()

    # add the prompt messages to the user messages
    chat = project_client.inference.get_chat_completions_client()
    return chat.complete(
        model="gpt-4o-mini",
        messages=system_message + messages,
        temperature=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )

if __name__ == "__main__":
    response = get_chat_response(
        messages=[{"role": "user", "content": "Can you instruct me on how to cook red pesto?"}],
        context={"name": "Alex"},
    )    

    # Clear terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    print(response.choices[0].message.content)