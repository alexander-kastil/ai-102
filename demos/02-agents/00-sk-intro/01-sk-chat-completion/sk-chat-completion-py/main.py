import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion
from semantic_kernel.connectors.ai.azure_ai_inference.azure_ai_inference_prompt_execution_settings import AzureAIInferencePromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.contents.text_content import TextContent
from semantic_kernel.contents.image_content import ImageContent

async def main():
    # Load environment variables
    load_dotenv()
    
    model = os.getenv("DEPLOYMENT_MODEL")
    endpoint = os.getenv("ENDPOINT")
    api_key = os.getenv("API_KEY")
    
    if not model:
        raise ValueError("DEPLOYMENT_MODEL is missing from environment variables.")
    if not endpoint:
        raise ValueError("ENDPOINT is missing from environment variables.")
    if not api_key:
        raise ValueError("API_KEY is missing from environment variables.")
    
    # Create kernel
    kernel = Kernel()
    
    # Add Azure AI Inference chat completion service
    chat_completion = AzureAIInferenceChatCompletion(
        ai_model_id=model,
        api_key=api_key,
        endpoint=endpoint,
        service_id="chat-gpt"
    )
    kernel.add_service(chat_completion)
    
    # Create execution settings
    execution_settings = AzureAIInferencePromptExecutionSettings(
        max_tokens=1000,
        temperature=0.7
    )
    
    # Create chat history
    history = ChatHistory()
    history.add_system_message("You are a helpful poetic assistant.")
    history.add_user_message("Tell me a short poem about whippets and the sea.")
    
    # Get response
    print("Getting response from AI...")
    try:
        response = await chat_completion.get_chat_message_contents(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel
        )
        if response:
            print(response[0].content)
        else:
            print("No response received")
    except Exception as e:
        print(f"Error getting response: {e}")
        return
    
    print("\n\nNow let's try an image to demonstrate multimodal capabilities.")
    
    # Read image file
    image_path = Path("data/soi-beach.jpg")
    if image_path.exists():
        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            
            # Add multimodal message
            history.add_user_message([
                TextContent(text="What is this image about?"),
                ImageContent(data=image_bytes, mime_type="image/jpeg")
            ])
            
            # Get response for image
            reply = await chat_completion.get_chat_message_contents(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel
            )
            if reply:
                print(reply[0].content)
        except Exception as e:
            print(f"Multimodal functionality might not be available: {e}")
    else:
        print("Image file not found. Skipping multimodal demonstration.")

if __name__ == "__main__":
    asyncio.run(main())