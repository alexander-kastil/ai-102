import os
import sys
from dotenv import load_dotenv
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import CodeInterpreterTool
from azure.ai.agents.models import FilePurpose, MessageAttachment, MessageRole
from azure.identity import DefaultAzureCredential
from pathlib import Path
from sandbox_downloader import SandboxDownloader
from banner import print_banner

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    # Clear the console to keep the output focused on the agent interaction
    os.system('cls' if os.name == 'nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    endpoint = os.getenv("PROJECT_ENDPOINT")
    model = os.getenv("MODEL_DEPLOYMENT")

    print(f"Using endpoint: {endpoint}")
    print(f"Using model: {model}")

    asset_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "assets", "quarterly_results.csv")
    )

    agents_client = AgentsClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    with agents_client:
        # Upload a file and wait for it to be processed
        # [START upload_file_and_create_agent_with_code_interpreter]
        file = agents_client.files.upload_and_poll(file_path=asset_file_path, purpose=FilePurpose.AGENTS)
        print(f"Uploaded file, file ID: {file.id}")

        code_interpreter = CodeInterpreterTool(file_ids=[file.id])

        # Create agent with code interpreter tool and tools_resources
        agent = agents_client.create_agent(
            model=model,
            name="code-interpreter-agent",
            instructions="You are a helpful agent with access to code interpreter tools. Use the code interpreter to analyze uploaded files and create visualizations as requested. Provide images directly in your response.",
            description="Demonstrates Code Interpreter tool for analyzing CSV files and generating data visualizations (charts/graphs) in a sandboxed Python environment.",
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        # [END upload_file_and_create_agent_with_code_interpreter]
        print(f"Created agent, agent ID: {agent.id}")

        thread = agents_client.threads.create()
        print(f"Created thread, thread ID: {thread.id}")

        # Create a message
        prompt = (
            "Could you please create a bar chart for the operating profit in the TRANSPORTATION "
            "sector from the uploaded csv file and display it as an image?"
        )
        print_banner(f"Prompt: {prompt}")
        message = agents_client.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt,
            attachments=[
                MessageAttachment(
                    file_id=file.id,
                    tools=code_interpreter.definitions,
                )
            ],
        )
        print(f"Created message, message ID: {message.id}")

        # Create the run and poll status + steps for real-time progress
        run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
        print(f"Run created with status: {run.status}")

        import time
        seen_step_status = {}
        last_status = None
        while True:
            run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
            if run.status != last_status:
                print(f"Run status: {run.status}")
                last_status = run.status

            steps = agents_client.run_steps.list(thread_id=thread.id, run_id=run.id)
            for step in steps:
                sid = step.get('id')
                st = step.get('status')
                prev = seen_step_status.get(sid)
                if prev != st:
                    print(f"Step {sid} status: {st}")
                    seen_step_status[sid] = st
                    step_details = step.get('step_details', {})
                    tool_calls = step_details.get('tool_calls', [])
                    if tool_calls:
                        print("  Tool calls:")
                        for call in tool_calls:
                            print(f"    Tool Call ID: {call.get('id')}")
                            print(f"    Type: {call.get('type')}")
                            code_details = call.get('code_interpreter', {})
                            if code_details:
                                if 'input' in code_details:
                                    print(f"    code_interpreter input: {code_details.get('input')}")
                                if 'output' in code_details:
                                    print(f"    code_interpreter output: {code_details.get('output')}")

            if run.status in ("completed", "failed", "cancelled"):
                print(f"Run finished with status: {run.status}")
                break

            time.sleep(1)

        if run.status == "failed":
            # Check if you got "Rate limit is exceeded.", then you want to get more quota
            print(f"Run failed: {run.last_error}")

        # [START get_messages_and_save_files]
        messages = agents_client.messages.list(thread_id=thread.id)
        for message in messages:
            if message.role != MessageRole.AGENT:
                continue
            for message_text in message.text_messages:
                print_banner(f"Agent Response:\n\n{message_text.text.value}")

        downloader = SandboxDownloader(agents_client)
        downloader.download(messages)
        # [END get_messages_and_save_files]

        last_msg = agents_client.messages.get_last_message_text_by_role(thread_id=thread.id, role=MessageRole.AGENT)
        if last_msg:
            print(f"Last Message: {last_msg.text.value}")

        agents_client.files.delete(file.id)
        print("Deleted file")

        delete_on_exit = os.getenv("DELETE_AGENT_ON_EXIT", "true").lower() == "true"
        if delete_on_exit:
            agents_client.delete_agent(agent.id)
            print("Deleted agent")
        else:
            print(f"Agent {agent.id} preserved for examination in Azure AI Foundry")


if __name__ == '__main__':
    main()
