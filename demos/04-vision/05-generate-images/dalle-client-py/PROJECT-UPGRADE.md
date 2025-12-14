# Project Upgrade: DALL-E Image Generator to Azure AI Foundry

## Overview

This project migrates from standalone Azure OpenAI DALL-E to **Azure AI Foundry** with project-scoped authentication and unified model management.

## Current State

- **Service**: Azure OpenAI (DALL-E image generation)
- **Authentication**: DefaultAzureCredential with API key fallback
- **SDK**: `openai`, `azure-identity`
- **Config Vars**: `ENDPOINT`, `MODEL_DEPLOYMENT`, `API_VERSION`

## Migration to Azure AI Foundry

### Key Changes

#### 1. Environment Configuration

**Current (.env)**:

```
ENDPOINT=https://your-resource.openai.azure.com/
MODEL_DEPLOYMENT=dalle3
API_VERSION=2024-02-01
```

**New (.env) - Using Foundry Project**:

```
PROJECT_ENDPOINT=https://pro-code-agents-resource.services.ai.azure.com/api/projects/pro-code-agents
MODEL_DEPLOYMENT=dalle3
API_VERSION=2024-10-21
```

#### 2. Authentication Method

**Current**:

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(exclude_environment_credential=True,
        exclude_managed_identity_credential=True),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider
)
```

**New (Recommended - Using Foundry Project)**:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

openai_client = project_client.get_openai_client(api_version="2024-10-21")
```

### Deployment Requirements

#### DALL-E Image Generation Model

You **must** have a DALL-E model deployment in your Foundry project:

- **Model**: DALL-E 3
- **Deployment Name**: Set in `MODEL_DEPLOYMENT` environment variable (default: "dalle3")
- **Location**: Same region as your Foundry project (recommended)
- **API Version**: 2024-02-01 or later

### Deployment Steps (Azure Portal or CLI)

#### Option 1: Using Azure Portal

1. Navigate to Azure AI Foundry portal
2. Go to your project → Models + Endpoints
3. Deploy DALL-E 3 model
4. Note the deployment name
5. Set `MODEL_DEPLOYMENT` environment variable

#### Option 2: Using Azure CLI

```bash
az cognitiveservices account deployment create \
  --resource-group <resource-group> \
  --name <foundry-resource> \
  --deployment-id dalle3 \
  --model-name dalle3 \
  --model-version "3.0"
```

#### Option 3: Using Bicep/Terraform

See Azure AI Foundry sample templates for infrastructure-as-code deployment.

## Step-by-Step Migration

1. **Update Dependencies**:

   ```bash
   pip install --upgrade azure-ai-projects azure-identity openai
   ```

2. **Create/Update .env**:

   ```
   PROJECT_ENDPOINT=https://pro-code-agents-resource.services.ai.azure.com/api/projects/pro-code-agents
   MODEL_DEPLOYMENT=dalle3
   API_VERSION=2024-10-21
   ```

3. **Update Code**:

   - Replace direct `AzureOpenAI` client with project client
   - Simplify authentication to use `DefaultAzureCredential` directly

4. **Deploy DALL-E Model**:

   - Use Azure Portal or CLI to deploy DALL-E 3
   - Verify deployment name matches `MODEL_DEPLOYMENT`

5. **Test Authentication**:
   - Run `az login` to authenticate
   - Verify project access

## Code Example - Updated

```python
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Import new Foundry SDK
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

def main():
    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get configuration settings
        load_dotenv()
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize Foundry project client
        project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential()
        )

        # Get OpenAI client from project
        client = project_client.get_openai_client(api_version="2024-10-21")

        img_no = 0

        # Interactive loop for image generation
        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Generate an image
            result = client.images.generate(
                model=model_deployment,
                prompt=input_text,
                n=1,
                size="1024x1024"
            )

            # Save the image
            image_url = result.data[0].url
            img_no += 1

            # Optionally download and save the image
            print(f"Image {img_no} generated successfully!")
            print(f"URL: {image_url}\n")

    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    main()
```

## Enhanced Version with Image Download

```python
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from PIL import Image
from io import BytesIO

def download_and_save_image(image_url: str, filename: str) -> str:
    """Download image from URL and save locally."""
    response = requests.get(image_url)
    response.raise_for_status()

    # Create images directory if needed
    images_dir = Path("generated_images")
    images_dir.mkdir(exist_ok=True)

    filepath = images_dir / filename
    with open(filepath, "wb") as f:
        f.write(response.content)

    return str(filepath)

def main():
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        load_dotenv()
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential()
        )

        client = project_client.get_openai_client(api_version="2024-10-21")

        img_no = 0

        while True:
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            print("Generating image...")

            result = client.images.generate(
                model=model_deployment,
                prompt=input_text,
                n=1,
                size="1024x1024"
            )

            image_url = result.data[0].url
            img_no += 1

            # Download and save image
            filename = f"generated_{img_no}.png"
            filepath = download_and_save_image(image_url, filename)
            print(f"Image saved to: {filepath}\n")

    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    main()
```

## Troubleshooting

### DALL-E Model Not Found

- **Error**: "The deployment 'dalle3' could not be found"
- **Solution**:
  - Verify DALL-E 3 is deployed in your Foundry project
  - Check deployment name matches `MODEL_DEPLOYMENT` variable
  - Use Azure Portal to confirm deployment status

### Authentication Issues

- **Error**: "DefaultAzureCredential authentication failed"
- **Solution**:
  - Run `az login` to authenticate to Azure
  - Verify account has access to Foundry project
  - Check subscription and resource group

### API Version Issues

- **Error**: "Unsupported API version"
- **Solution**:
  - Use API version 2024-02-01 or later for DALL-E 3
  - Update to 2024-10-21 when using Foundry project client

### Image Generation Timeout

- **Error**: "Request timed out"
- **Solution**:
  - DALL-E generation can take 30-60 seconds
  - Consider async operations for production
  - Check quota limits on model deployment

## Performance Notes

### Generation Time

- First image: 30-60 seconds typically
- Subsequent images: Similar time
- Consider adding async support for better UX

### Cost Optimization

- Monitor usage through Foundry portal
- DALL-E 3 pricing is based on image size and quality
- Consider batch operations for multiple images

### Quality Settings (DALL-E 3)

```python
result = client.images.generate(
    model=model_deployment,
    prompt=input_text,
    n=1,
    size="1024x1024",  # Options: 1024x1024, 1792x1024, 1024x1792
    quality="standard",  # Options: standard, hd
    style="vivid"  # Options: natural, vivid
)
```

## Related Resources

- [Azure AI Foundry Quickstart](https://learn.microsoft.com/en-us/azure/ai-foundry/quickstarts/get-started-code)
- [DALL-E Image Generation Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/dall-e-quickstart)
- [Azure AI Projects SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme)
- [OpenAI Python Client](https://github.com/openai/openai-python)

## Notes

- DALL-E 3 model **must be deployed** before this application can run
- Deployment takes ~5-10 minutes
- Monitor costs - image generation incurs charges
- Consider implementing async operations for production
- Consider adding progress indicators for better UX during generation
