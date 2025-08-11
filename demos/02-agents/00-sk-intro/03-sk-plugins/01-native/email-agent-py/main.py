import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.azure_open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from common.config import AppConfig
from plugins.email_plugin import EmailPlugin

async def main():
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    config = AppConfig.from_env()
    
    # Validate configuration
    if not config.deployment_model:
        raise ValueError("DEPLOYMENT_MODEL is missing from environment variables.")
    if not config.endpoint:
        raise ValueError("ENDPOINT is missing from environment variables.")
    if not config.api_key:
        raise ValueError("API_KEY is missing from environment variables.")
    
    # Create kernel
    kernel = Kernel()
    
    # Add Azure OpenAI chat completion service
    chat_completion = AzureChatCompletion(
        deployment_name=config.deployment_model,
        api_key=config.api_key,
        endpoint=config.endpoint,
        service_id="chat-gpt"
    )
    kernel.add_service(chat_completion)
    
    # Create and add email plugin
    email_plugin = EmailPlugin(config.graph_config)
    kernel.add_plugin(email_plugin, plugin_name="EmailPlugin")
    
    # Create chat history with system message
    history = ChatHistory()
    history.add_system_message("""
    You are a friendly assistant who likes to follow the rules. You will complete required steps
    and request approval before taking any consequential actions. If the user doesn't provide
    enough information for you to complete a task, you will keep asking questions until you have
    enough information to complete the task.
    """)
    
    # Start the conversation loop
    print("Email Agent is ready! Type 'quit' to exit.")
    
    while True:
        # Get user input
        user_input = input("How can I help you?: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
            
        history.add_user_message(user_input)
        
        # Configure execution settings for function calling
        execution_settings = OpenAIChatPromptExecutionSettings(
            tool_choice="auto",
            function_call_behavior=FunctionCallBehavior.EnableFunctions(
                auto_invoke=True, filters={}
            )
        )
        
        try:
            # Get streaming response
            response = chat_completion.get_streaming_chat_message_contents(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel
            )
            
            # Stream and collect the response
            full_message = ""
            async for chunk in response:
                if chunk[0].content:
                    print(chunk[0].content, end="", flush=True)
                    full_message += chunk[0].content
            
            print()  # New line after streaming
            
            # Add assistant message to history
            if full_message:
                history.add_assistant_message(full_message)
                
        except Exception as e:
            print(f"Error: {str(e)}")
            continue

if __name__ == "__main__":
    asyncio.run(main())