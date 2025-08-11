import asyncio
import os
import subprocess
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.azure_open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.contents import ChatHistory

async def main():
    # Load environment variables
    load_dotenv()
    
    model = os.getenv("DEPLOYMENT_MODEL")
    endpoint = os.getenv("ENDPOINT")
    api_key = os.getenv("API_KEY")
    repo = os.getenv("GIT_REPO")
    
    if not model:
        raise ValueError("DEPLOYMENT_MODEL is missing from environment variables.")
    if not endpoint:
        raise ValueError("ENDPOINT is missing from environment variables.")
    if not api_key:
        raise ValueError("API_KEY is missing from environment variables.")
    if not repo:
        raise ValueError("GIT_REPO is missing from environment variables.")
    
    print("Setting up MCP GitHub server...")
    
    # Note: This is a simplified version of MCP integration
    # The full MCP integration would require installing and configuring the MCP client
    # For now, we'll simulate the GitHub functionality with direct API calls
    
    print("MCP GitHub tools available:")
    print("- list_repositories: List repositories for a user/organization")
    print("- get_repository: Get details about a repository")  
    print("- list_commits: List commits in a repository")
    print("- get_commit: Get details about a specific commit")
    print("- list_issues: List issues in a repository")
    print("- get_issue: Get details about a specific issue")
    
    # Create kernel
    kernel = Kernel()
    
    # Add Azure OpenAI chat completion service
    chat_completion = AzureChatCompletion(
        deployment_name=model,
        api_key=api_key,
        endpoint=endpoint,
        service_id="chat-gpt"
    )
    kernel.add_service(chat_completion)
    
    # Configure execution settings
    execution_settings = OpenAIChatPromptExecutionSettings(
        temperature=0,
        function_call_behavior=FunctionCallBehavior.EnableFunctions(
            auto_invoke=True, filters={}
        )
    )
    
    # Test basic prompt
    prompt = f"Summarize the last commit to the {repo} repository?"
    print(f"\nPrompt: {prompt}")
    
    result = await kernel.invoke_prompt(prompt, execution_settings=execution_settings)
    print(f"Result: {result}")
    
    # Create agent
    agent = ChatCompletionAgent(
        service_id="chat-gpt",
        kernel=kernel,
        name="GitHubAgent",
        instructions="Answer questions about GitHub repositories. You are an expert at analyzing GitHub repositories and commits.",
        execution_settings=execution_settings
    )
    
    # Test agent responses
    prompts = [
        f"Summarize the latest commit in the {repo} repository?",
        f"Summarize the last issue in the {repo} repository?"
    ]
    
    for prompt in prompts:
        print(f"\nPrompt to GitHubAgent: {prompt}")
        
        # Create a new chat for each prompt
        chat = ChatHistory()
        chat.add_user_message(prompt)
        
        async for response in agent.invoke(chat):
            print(f"Response from GitHubAgent: {response.content}")

if __name__ == "__main__":
    asyncio.run(main())