# Project Upgrade: Face Detection API to Azure AI Foundry

## Overview
This project migrates from standalone Azure AI Vision Face API to **Azure AI Foundry** for unified resource management and authentication using project endpoints.

## Current State
- **Service**: Azure AI Vision Face API
- **Authentication**: API Key (AI_SERVICE_ENDPOINT, AI_SERVICE_KEY)
- **SDK**: `azure-ai-vision-face==1.0.0b2`

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
FACE_ENDPOINT=https://your-face-resource.cognitiveservices.azure.com/
```

#### 2. Authentication Method
**Current**:
```python
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceClient

face_client = FaceClient(
    endpoint=cog_endpoint,
    credential=AzureKeyCredential(cog_key)
)
```

**New (Recommended)**:
```python
from azure.identity import DefaultAzureCredential
from azure.ai.vision.face import FaceClient

face_client = FaceClient(
    endpoint=face_endpoint,
    credential=DefaultAzureCredential()
)
```

### Deployment Requirements

#### Azure AI Vision (Face) Service
You **must** have an Azure AI Vision resource with Face capabilities:
- Resource Type: `Cognitive Services account` (Computer Vision)
- Capabilities: `Face API`
- Location: Same region as your Foundry project (recommended)

**No new vision model deployments needed** - the face services work with resource-level endpoints, not model deployments.

### Step-by-Step Migration

1. **Update Dependencies**:
   ```bash
   pip install --upgrade azure-identity azure-ai-vision-face
   ```

2. **Update Environment Variables**:
   - Set `PROJECT_ENDPOINT` to your Foundry project endpoint
   - Set `FACE_ENDPOINT` to your Azure AI Vision Face resource endpoint
   - Remove `AI_SERVICE_KEY`

3. **Update Code**:
   - Replace `AzureKeyCredential` with `DefaultAzureCredential`
   - Update endpoint to Face resource endpoint
   - Ensure Azure CLI login: `az login`

4. **Permissions**:
   - Ensure your Azure account has `Cognitive Services User` role on the Face resource
   - Or use Managed Identity if running in Azure

### Code Example - Updated

```python
from dotenv import load_dotenv
import os
import sys
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel, FaceAttributeTypeDetection01
from azure.identity import DefaultAzureCredential  # Changed from AzureKeyCredential

def main():
    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        # Get Configuration Settings
        load_dotenv()
        face_endpoint = os.getenv('FACE_ENDPOINT')  # Face resource endpoint

        # Get image
        image_file = 'images/face1.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        # Authenticate Face client with Entra ID
        face_client = FaceClient(
            endpoint=face_endpoint,
            credential=DefaultAzureCredential()  # Changed
        )

        # Specify facial features to be retrieved
        features = [FaceAttributeTypeDetection01.HEAD_POSE,
                    FaceAttributeTypeDetection01.OCCLUSION,
                    FaceAttributeTypeDetection01.ACCESSORIES]

        # Get faces
        with open(image_file, mode="rb") as image_data:
            detected_faces = face_client.detect(
                image_content=image_data.read(),
                detection_model=FaceDetectionModel.DETECTION01,
                recognition_model=FaceRecognitionModel.RECOGNITION01,
                return_face_id=False,
                return_face_attributes=features,
            )

        # Rest of the code remains the same
        ...
```

## Troubleshooting

### Authentication Issues
- **Error**: "DefaultAzureCredential authentication failed"
  - **Solution**: Run `az login` to authenticate to Azure
  - Verify your account has permissions on the Face resource

### Endpoint Issues
- **Error**: "Invalid endpoint URL"
  - **Solution**: Use the Face resource endpoint
  - Format: `https://<resource-name>.cognitiveservices.azure.com/`

### Missing Face Resource
- **Error**: "Resource not found"
  - **Solution**: Create an Azure AI Vision (Computer Vision) resource with Face capability in Azure Portal
  - Wait for deployment to complete

### SDK Version Compatibility
- Current: `azure-ai-vision-face==1.0.0b2` (beta)
- May need to upgrade to stable version when available
- Update: `pip install --upgrade azure-ai-vision-face`

## Related Resources
- [Azure Face API Documentation](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-identity)
- [Azure AI Foundry Overview](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [DefaultAzureCredential Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme)

## Notes
- This project detects and analyzes faces in images - no model deployment needed
- The Azure AI Face service is fully compatible with Foundry projects
- Consider using managed identity in production for better security
- Face API SDK is still in beta - monitor for stable release updates
