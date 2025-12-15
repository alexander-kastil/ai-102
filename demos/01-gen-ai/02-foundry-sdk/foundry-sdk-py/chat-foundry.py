from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

chat = project_client.get_openai_client()
# Prepare messages
system_message = (
    "You are an AI assistant that speaks like a techno punk rocker from 2350. "
    "Be cool but not too cool. Ya dig?"
)
user_message = "Hey, can you help me with my taxes? I'm a freelancer."

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message},
]

# Helper to print a simple banner
def _print_banner(title: str, content: str, width: int = 80) -> None:
    line = "=" * width
    sub = "-" * width
    print(line)
    print(title.center(width))
    print(sub)
    print(content)
    print(line)

# Clear and print banner before calling the model
os.system('cls' if os.name == 'nt' else 'clear')
_print_banner("System Message", system_message)
_print_banner("User Prompt", user_message)

# Call the model
response = chat.chat.completions.create(
    model=os.environ["MODEL"],
    messages=messages,
)

print(response.choices[0].message.content)