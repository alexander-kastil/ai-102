from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]
router_model = os.environ["MODEL_ROUTER"]

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()

# Prepare messages
system_message = "You are a helpful assistant."
user_message = (
    "Write a comprehensive account of solo backpacking adventure through South America, "
    "covering countries like Colombia, Peru, Bolivia, and Argentina. Detail the challenges "
    "and triumphs of traveling solo, your interactions with locals, and the cultural diversity "
    "you encountered along the way. Include must-visit attractions, unique experiences like hiking "
    "the Inca Trail or exploring Patagonia, and recommendations for budget travelers. Provide a "
    "structured itinerary, a cost breakdown, and safety tips for solo adventurers in the region."
)

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

# Clear and print banners before calling the model
os.system('cls' if os.name == 'nt' else 'clear')
_print_banner("System Message", system_message)
_print_banner("User Prompt", user_message)

response = client.chat.completions.create(
    messages=messages,
    max_tokens=8192,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model=router_model
)

print("=" * 50)
print(f"Model chosen by the router: {response.model}")
print("=" * 50)
print(response.choices[0].message.content)