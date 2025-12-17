import os
import time
import io
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from openai import OpenAI  # type: ignore
import qrcode
from datetime import datetime
from azure.storage.blob import BlobServiceClient

# This demo shows post-processing of agent responses and external integration.
# It creates an agent, streams its response, captures the output, generates a QR code
# from user input, and uploads it to Azure Blob Storage.

def generate_qr_code(content: str, storage_connection_string: str, storage_container_name: str) -> str:
    # Generate QR image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    # Upload to blob storage
    date_str = datetime.now().strftime("%Y%m%d")
    blob_name = f"qr{date_str}.jpg"

    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_client = blob_service_client.get_container_client(storage_container_name)
    try:
        container_client.create_container()
        print(f"Created container {storage_container_name}")
    except Exception as e:
        if "ContainerAlreadyExists" not in str(e):
            raise
    blob_client = blob_service_client.get_blob_client(container=storage_container_name, blob=blob_name)
    blob_client.upload_blob(img_bytes, overwrite=True)

    # Construct download URL (account host assumed per existing pattern)
    download_url = f"https://procodestorageacct.blob.core.windows.net/{storage_container_name}/{blob_name}"
    return download_url


def main():

    # Clear the console to keep the output focused on the agent interaction
    os.system('cls' if os.name == 'nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    endpoint = os.getenv("PROJECT_ENDPOINT")
    model = os.getenv("MODEL_DEPLOYMENT")
    storage_connection_string = os.getenv("STORAGE_CONNECTION_STRING")
    storage_container_name = os.getenv("STORAGE_CONTAINER_NAME")

    delete_resources = os.getenv("DELETE", "true").lower() == "true"
    print(f"Using endpoint: {endpoint}")
    print(f"Using model: {model}")
    print(f"Delete resources: {delete_resources}")

    # Initialize new project + responses client (no threads/runs now)
    project_client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    openai_client: OpenAI = project_client.get_openai_client()
    with project_client:
        start = time.time()
        agent = project_client.agents.create_version(
            agent_name="output-agent",
            definition=PromptAgentDefinition(
                model=model,
                instructions=(
                    "You are a helpful agent. When asked to generate a QR code, "
                    "call the generate_qr_code function tool with the 'content' to encode, "
                    "then return the resulting download URL."
                ),
                tools=[
                    FunctionTool(
                        name="generate_qr_code",
                        description=(
                            "Generate a QR code for the provided content, upload to Azure Blob Storage, "
                            "and return the public download URL."
                        ),
                        parameters={
                            "type": "object",
                            "properties": {
                                "content": {
                                    "type": "string",
                                    "description": "The text/URL to encode into a QR code."
                                }
                            },
                            "required": ["content"]
                        }
                    )
                ]
            )
        )
        print(f"Created agent: {agent.name} (version {agent.version})")

        # Ask for QR code content (agent will call tool)
        user_input = input("What do you want to encode? Press Enter for default: https://www.integrations.at\n")
        qr_content = user_input if user_input.strip() else "https://www.integrations.at"

        # Define function tool for the agent
        tool_def = {
            "type": "function",
            "function": {
                "name": "generate_qr_code",
                "description": "Generate a QR code for the provided content, upload it to Azure Blob Storage, and return the download URL.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "The text/URL to encode into a QR code."}
                    },
                    "required": ["content"]
                }
            }
        }

        # Create a response prompting the agent to use the tool
        try:
            response = openai_client.responses.create(
                input=f"Please generate a QR code for: {qr_content} and provide the download URL.",
                extra_body={
                    "agent": {"type": "agent_reference", "name": agent.name, "version": agent.version}
                }
            )
        except Exception as e:
            print(f"Response creation failed: {e}")
            if delete_resources:
                project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
                print("Deleted agent version after failure")
            response = None

        # If the agent requested tool calls, execute them and submit outputs
        final_response = None
        if response:
            try:
                required_action = getattr(response, "required_action", None)
                tool_calls = []
                if required_action and hasattr(required_action, "submit_tool_outputs"):
                    sto = required_action.submit_tool_outputs
                    for tc in getattr(sto, "tool_calls", []):
                        try:
                            func = tc.function
                            if func.name == "generate_qr_code":
                                args = json.loads(func.arguments or "{}")
                                content = args.get("content", qr_content)
                                url = generate_qr_code(content, storage_connection_string, storage_container_name)
                                tool_calls.append({"tool_call_id": tc.id, "output": url})
                        except Exception as te:
                            print(f"Tool execution error: {te}")
                    if tool_calls:
                        final_response = openai_client.responses.submit_tool_outputs(
                            response_id=response.id,
                            tool_outputs=tool_calls
                        )
                else:
                    # No tool calls required; use the original response as final
                    final_response = response
            except Exception as e:
                print(f"Failed handling tool calls: {e}")
                final_response = response

        # Print the final agent message if available
        if final_response:
            try:
                duration = time.time() - start
                print(f"Response completed (took {duration:.2f}s)")
                output_text = getattr(final_response, "output_text", None)
                if output_text:
                    print("agent: ", output_text)
                else:
                    print("Agent responded.")
            except Exception as e:
                print(f"Error printing final response: {e}")

        if delete_resources:
            project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
            print("Deleted agent version")
        else:
            print(f"Preserved agent: {agent.name}:{agent.version}")

        # No local QR generation here; handled by the agent tool.


if __name__ == '__main__':
    main()
