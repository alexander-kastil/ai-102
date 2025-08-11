"""Main entry point for the email agent using Semantic Kernel."""

import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.azure_openai import AzureOpenAIChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

from common.app_config import AppConfig
from plugins.email_plugin import EmailPlugin


async def main():
    """Main function to run the email agent."""
    # Load configuration
    config = AppConfig.from_env()
    
    # Validate configuration
    if not all([config.semantic_kernel.endpoint, config.semantic_kernel.api_key]):
        print("Error: Missing Semantic Kernel configuration. Please check your .env file.")
        return
        
    if not all([config.graph.tenant_id, config.graph.client_id, 
                config.graph.client_secret, config.graph.mail_sender]):
        print("Error: Missing Graph configuration. Please check your .env file.")
        return

    # Create kernel
    kernel = Kernel()

    # Add Azure OpenAI chat completion service
    chat_completion = AzureOpenAIChatCompletion(
        deployment_name=config.semantic_kernel.model,
        api_key=config.semantic_kernel.api_key,
        endpoint=config.semantic_kernel.endpoint,
    )
    
    kernel.add_service(chat_completion)

    # Create and add email plugin
    email_plugin = EmailPlugin(config.graph)
    kernel.add_plugin(email_plugin, plugin_name="EmailPlugin")

    # Create chat history with system message
    history = ChatHistory()
    history.add_system_message("""
    You are a friendly assistant who likes to follow the rules. You will complete required steps
    and request approval before taking any consequential actions. If the user doesn't provide
    enough information for you to complete a task, you will keep asking questions until you have
    enough information to complete the task.
    """)

    print("Email Agent is ready! Type your requests below.")
    print("You can ask me to send emails to specific recipients.")
    print("Type 'exit' to quit.\n")

    # Start conversation loop
    while True:
        try:
            # Get user input
            user_input = input("How can I help you?: ")
            
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            # Add user message to history
            history.add_user_message(user_input)

            # Configure function choice behavior for tool calls
            execution_settings = chat_completion.get_prompt_execution_settings_class()(
                function_choice_behavior=FunctionChoiceBehavior.Auto()
            )

            # Get streaming response
            response = chat_completion.get_streaming_chat_message_contents(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel
            )

            # Stream and collect the response
            full_message = ""
            async for content in response:
                if content.content:
                    print(content.content, end="", flush=True)
                    full_message += content.content

            print()  # New line after streaming

            # Add assistant message to history
            if full_message:
                history.add_assistant_message(full_message)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())