import os
try:
    from dotenv import load_dotenv
except ImportError:
    print("Installing python-dotenv package...")
    import subprocess
    subprocess.check_call(["pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

try:
    from openai import AzureOpenAI
except ImportError:
    print("Installing openai package...")
    import subprocess
    subprocess.check_call(["pip", "install", "openai"])
    from openai import AzureOpenAI


def main(): 
    try: 
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=azure_oai_endpoint,
            api_key=azure_oai_key,
            api_version="2024-02-15-preview"
        )



        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            print("\nSending request for summary to Azure OpenAI endpoint...\n")

            system_message = """I am a hiking enthusiast named Forest who helps people discover hikes in their area.
            If no area is specified, I will default to near Rainier National Park.
            I will then provide three suggestions for nearby hikes that vary in length.
            I will also share an interesting fact about the local nature on the hikes when making a recommendation.
            """
            
            # Send request to Azure OpenAI
            response = client.chat.completions.create(
                model=azure_oai_deployment,
                temperature=0.7,
                max_tokens=400,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": input_text}
                ]
            )
            generated_text = response.choices[0].message.content

            # Print the response
            print("Response: " + generated_text + "\n")
            
            

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()