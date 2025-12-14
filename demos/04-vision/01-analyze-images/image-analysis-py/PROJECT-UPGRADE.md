# Project Upgrade: Image Analysis to Azure AI Foundry

## Overview

This project migrates from standalone Azure AI Vision Image Analysis service to **Azure AI Foundry** for unified resource management and authentication using project endpoints.

## Current State

- **Service**: Azure AI Vision (Computer Vision)
- **Authentication**: API Key (AI_SERVICE_ENDPOINT, AI_SERVICE_KEY)
- **SDK**: `azure-ai-vision-imageanalysis==1.0.0`

## Migration to Azure AI Foundry

### Benefits

- **Unified Authentication**: Use project endpoint with Azure Entra ID instead of API keys
- **Keyless Security**: Microsoft Entra ID authentication eliminates API key management
- **Integrated Resource Management**: Single project endpoint for multiple Azure AI services
- **Project Context**: All resources scoped to a specific AI Foundry project

### Key Changes

#### 1. Environment Configuration

**Current (.env)**:

```
AI_SERVICE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AI_SERVICE_KEY=your-api-key
```

**New (.env)**:

```
PROJECT_ENDPOINT=https://pro-code-agents-resource.services.ai.azure.com/api/projects/pro-code-agents
```

#### 2. Authentication Method

**Current**:

```python
from azure.core.credentials import AzureKeyCredential
cv_client = ImageAnalysisClient(
    endpoint=ai_endpoint,
    credential=AzureKeyCredential(ai_key)
)
```

**New - Option A (Recommended - Direct Image Analysis)**:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient

cv_client = ImageAnalysisClient(
    endpoint=endpoint,  # Use the Azure AI Vision resource endpoint
    credential=DefaultAzureCredential()
)
```

**New - Option B (Using AI Foundry Project Client)**:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)
# Then get specific service clients as needed
```

### Deployment Requirements

#### Azure AI Vision Service

You **must** have an Azure AI Vision resource deployed in your Azure subscription:

- Resource Type: `Cognitive Services account` (Computer Vision)
- Endpoints: `Image Analysis` capability
- Location: Same region as your Foundry project (recommended)

**No new vision model deployments needed** - the vision services work with resource-level endpoints, not model deployments.

### Step-by-Step Migration

1. **Update Dependencies**:

   ```bash
   pip install --upgrade azure-identity azure-ai-vision-imageanalysis
   ```

2. **Update Environment Variables**:

   - Set `PROJECT_ENDPOINT` to your Foundry project endpoint
   - Optionally keep `VISION_ENDPOINT` pointing to your Azure AI Vision resource

3. **Update Code**:

   - Replace `AzureKeyCredential` with `DefaultAzureCredential`
   - Update endpoint to use Entra ID
   - Ensure Azure CLI login: `az login`

4. **Permissions**:
   - Ensure your Azure account has `Cognitive Services User` role on the Vision resource
   - Or use Managed Identity if running in Azure

### Code Example - Updated

```python
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
import sys
from matplotlib import pyplot as plt
from azure.core.exceptions import HttpResponseError
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.identity import DefaultAzureCredential  # Changed from AzureKeyCredential

def main():
    global cv_client
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('VISION_ENDPOINT')  # Azure AI Vision resource endpoint

        # Get image
        image_file = 'images/street.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        with open(image_file, "rb") as f:
            image_data = f.read()

        # Authenticate Azure AI Vision client with Entra ID
        cv_client = ImageAnalysisClient(
            endpoint=ai_endpoint,
            credential=DefaultAzureCredential()  # Changed
        )
        print('Client created')

        # Rest of the code remains the same
        AnalyzeImage(image_file, image_data, cv_client)

    except Exception as ex:
        print(ex)
```

## Troubleshooting

### Authentication Issues

- **Error**: "DefaultAzureCredential authentication failed"
  - **Solution**: Run `az login` to authenticate to Azure
  - Verify your account has permissions on the Vision resource

### Endpoint Issues

- **Error**: "Invalid endpoint URL"
  - **Solution**: Use the Vision resource endpoint, not the Foundry project endpoint
  - Format: `https://<resource-name>.cognitiveservices.azure.com/`

### Missing Vision Resource

- **Error**: "Resource not found"
  - **Solution**: Create an Azure AI Vision (Computer Vision) resource in Azure Portal
  - Wait for deployment to complete

## Related Resources

- [Azure AI Vision Documentation](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)
- [Azure AI Foundry Overview](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [DefaultAzureCredential Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme)

## Notes

- This project analyzes images locally - no model deployment needed
- The Azure AI Vision service is fully compatible with Foundry projects
- Consider using managed identity in production for better security
