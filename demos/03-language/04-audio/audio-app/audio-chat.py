import os
import requests
import base64
from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential

def main(): 

    try: 
        # Get configuration settings 
        load_dotenv()
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")

        print("Configuration:")
        print(f"  Endpoint: {project_endpoint}")
        print(f"  Model: {model_deployment}\n")

        # Initialize prompts
        system_message = "You are an AI assistant for a produce supplier company."
        prompt = "Who was calling, and what did they want?"

        print("Getting a response ...\n")

        # Fetch remote audio file
        print(f"Prompt: {prompt}\n")
        audio_url = "https://github.com/MicrosoftLearning/mslearn-ai-language/raw/refs/heads/main/Labfiles/09-audio-chat/data/avocados.mp3"
        print(f"Downloading audio...")
        audio_response = requests.get(audio_url)
        audio_response.raise_for_status()
        audio_bytes = audio_response.content
        audio_data = base64.b64encode(audio_bytes).decode('utf-8')
        print(f"Audio data encoded: {len(audio_data)} chars\n")

        # Use direct HTTP with bearer token
        from azure.identity import get_bearer_token_provider
        
        token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
        token = token_provider()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Extract resource name from endpoint and construct models endpoint
        resource_name = project_endpoint.split('/')[2].split('.')[0]
        base_url = f"https://{resource_name}.services.ai.azure.com"
        api_url = f"{base_url}/models/chat/completions?api-version=2024-05-01-preview"
        
        payload = {
            "model": model_deployment,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "input_audio", "input_audio": {"data": audio_data, "format": "mp3"}}
                ]}
            ]
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("Response:")
            print(result['choices'][0]['message']['content'])
        else:
            print(f"Error ({response.status_code}): {response.text}")

    except Exception as ex:
        print(f"Error: {ex}")

    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()