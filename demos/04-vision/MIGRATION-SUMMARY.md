# Azure AI Foundry Migration Summary - Vision Demos

## Overview

Migration guide for 4 Python projects in `demos/04-vision` to Azure AI Foundry with authentication using the provided project endpoint.

**Project Endpoint**: `https://pro-code-agents-resource.services.ai.azure.com/api/projects/pro-code-agents`

## Projects Summary

### 1. Image Analysis (`01-analyze-images/image-analysis-py`)

**Status**: ✅ Ready to Migrate  
**Current Service**: Azure AI Vision Image Analysis  
**Migration Type**: Service authentication upgrade  
**Model Deployments Needed**: ❌ None

**Key Changes**:

- Replace `AzureKeyCredential` with `DefaultAzureCredential`
- Update from API key to Entra ID authentication
- Point to Azure AI Vision resource (not Foundry project endpoint)

**Documentation**: See [PROJECT-UPGRADE.md](01-analyze-images/image-analysis-py/PROJECT-UPGRADE.md)

---

### 2. Face Detection (`02-detect-faces/face-api-py`)

**Status**: ✅ Ready to Migrate  
**Current Service**: Azure AI Vision Face API  
**Migration Type**: Service authentication upgrade  
**Model Deployments Needed**: ❌ None

**Key Changes**:

- Replace `AzureKeyCredential` with `DefaultAzureCredential`
- Update from API key to Entra ID authentication
- Point to Azure AI Vision Face resource (not Foundry project endpoint)

**Documentation**: See [PROJECT-UPGRADE.md](02-detect-faces/face-api-py/PROJECT-UPGRADE.md)

---

### 3. Gen AI Vision Chat (`04-gen-ai-vision/gen-ai-vision-py`)

**Status**: ✅ Already Foundry-Compatible  
**Current Service**: Azure OpenAI (GPT-4) + Azure AI Vision  
**Migration Type**: Configuration optimization  
**Model Deployments Needed**: ✅ Vision-capable model (GPT-4o or GPT-4 Turbo)

**Key Changes**:

- Already using `AIProjectClient` from `azure-ai-projects`
- Update environment variables to use `PROJECT_ENDPOINT`
- Ensure model deployment is vision-capable
- Optional: Add image analysis features

**Documentation**: See [PROJECT-UPGRADE.md](04-gen-ai-vision/gen-ai-vision-py/PROJECT-UPGRADE.md)

---

### 4. Image Generator - Upgrade to GPT-image-1 (`05-generate-images/dalle-client-py`)

**Status**: ✅ Ready to Migrate (+ Upgrade)  
**Current Service**: Azure OpenAI DALL-E 3  
**Recommended Upgrade**: **GPT-image-1** (State-of-the-art, April 2025)
**Migration Type**: Full Foundry integration + Model upgrade  
**Model Deployments Needed**: ✅ GPT-image-1 model deployment (limited access preview)

**Why Upgrade to GPT-image-1?**:

- ✅ **Better Text Rendering**: Excellent text in images (DALL-E 3 weakness)
- ✅ **Image Editing**: New capability to edit existing images
- ✅ **Superior Instruction Following**: Better prompt understanding
- ✅ **Inpainting**: Fill masked image regions (new capability)

**Key Changes**:

- Switch from direct `AzureOpenAI` client to `AIProjectClient`
- Update environment variables to use `PROJECT_ENDPOINT`
- Simplify authentication with `DefaultAzureCredential`
- **Deploy GPT-image-1 model** (request access: [aka.ms/oai/gptimage1access](https://aka.ms/oai/gptimage1access))
- Update API version to 2025-04-01-preview

**Documentation**: See [PROJECT-UPGRADE.md](05-generate-images/dalle-client-py/PROJECT-UPGRADE.md)

---

## Environment Configuration Template

Create/update `.env` files in each project:

### Image Analysis & Face Detection

```bash
# Use Azure AI Vision resource endpoint (not Foundry project endpoint)
VISION_ENDPOINT=https://your-vision-resource.cognitiveservices.azure.com/
FACE_ENDPOINT=https://your-vision-resource.cognitiveservices.azure.com/
```

### Gen AI Vision Chat

```bash
PROJECT_ENDPOINT=https://pro-code-agents-resource.services.ai.azure.com/api/projects/pro-code-agents
MODEL_DEPLOYMENT=gpt-4o
```

### Image Generator (GPT-image-1)

```bash
PROJECT_ENDPOINT=https://pro-code-agents-resource.services.ai.azure.com/api/projects/pro-code-agents
MODEL_DEPLOYMENT=gpt-image-1
API_VERSION=2025-04-01-preview
```

---

## Prerequisites

### For All Projects

1. **Azure Account**: Active subscription with access to Foundry project
2. **Azure CLI**: Installed and authenticated (`az login`)
3. **Python 3.8+**: With pip package manager
4. **Entra ID Permissions**: At least "Contributor" or service-specific roles

### Service-Specific Requirements

#### Image Analysis & Face Detection

- ✅ Azure AI Vision resource (Computer Vision)
- Location: Same region as Foundry project (recommended)
- Capabilities: Image Analysis and/or Face API

#### Gen AI Vision Chat

- ✅ Azure OpenAI resource with GPT-4o or GPT-4 Turbo deployment
- Vision API version: 2024-10-21 or later
- Capability: Must support vision features

#### Image Generator

- ✅ GPT-image-1 model deployment in Foundry project (limited access preview)
- Deployment name: Configure in `MODEL_DEPLOYMENT`
- Access Request: [aka.ms/oai/gptimage1access](https://aka.ms/oai/gptimage1access)
- Approval Timeline: Typically 24-48 hours
- Quota: Ensure sufficient image generation quota
- API Version: 2025-04-01-preview

---

## Migration Steps (Per Project)

### Step 1: Review Documentation

- Read the PROJECT-UPGRADE.md file in each project directory
- Understand current vs. new authentication patterns

### Step 2: Update Dependencies

```bash
cd <project-directory>
pip install --upgrade azure-identity azure-ai-projects openai azure-ai-vision-imageanalysis azure-ai-vision-face
```

### Step 3: Update Environment Configuration

- Copy `.env.example` (if exists) or create `.env`
- Add/update environment variables per the template above
- Do NOT commit `.env` file (add to `.gitignore`)

### Step 4: Update Code

- Replace `AzureKeyCredential` with `DefaultAzureCredential`
- Update client initialization code
- For Gen AI projects, use `AIProjectClient.get_openai_client()`

### Step 5: Test Authentication

```bash
# Authenticate to Azure
az login

# Run the project
python <script-name>.py
```

### Step 6: Deploy Models (if needed)

For projects requiring model deployments:

1. Go to Azure AI Foundry portal
2. Navigate to Models + Endpoints
3. Deploy required model
4. Verify deployment name

---

## Model Deployment Requirements Summary

| Project         | Model       | Type    | Required | Deployment Name |
| --------------- | ----------- | ------- | -------- | --------------- |
| Image Analysis  | Vision API  | Service | ❌ No    | N/A             |
| Face Detection  | Face API    | Service | ❌ No    | N/A             |
| Gen AI Vision   | GPT-4o      | Model   | ✅ Yes   | `gpt-4o`        |
| Image Generator | GPT-image-1 | Model   | ✅ Yes   | `gpt-image-1`   |

### How to Deploy Models

#### Azure Portal Method

1. Sign in to [Azure AI Foundry](https://ai.azure.com)
2. Navigate to your project
3. Go to "Models + Endpoints"
4. Click "Deploy model"
5. Select model and review deployment options
6. Complete deployment and note the deployment name

#### Azure CLI Method

```bash
# Deploy GPT-4o
az cognitiveservices account deployment create \
  --resource-group <rg-name> \
  --name <foundry-resource> \
  --deployment-id gpt-4o \
  --model-name gpt-4o \
  --model-version "2024-08-06"

# Deploy GPT-image-1 (requires limited access)
# Request access first at: https://aka.ms/oai/gptimage1access
az cognitiveservices account deployment create \
  --resource-group <rg-name> \
  --name <foundry-resource> \
  --deployment-id gpt-image-1 \
  --model-name gpt-image-1 \
  --model-version "1.0"
```

---

## Troubleshooting Common Issues

### Authentication Failures

```
Error: "DefaultAzureCredential authentication failed"
```

**Solution**:

- Run `az login` to authenticate
- Verify Azure subscription access
- Check account has sufficient permissions

### Endpoint Not Found

```
Error: "The endpoint 'https://...' is not valid"
```

**Solution**:

- Verify endpoint URL format
- For Vision services: Use resource endpoint, not Foundry project endpoint
- For Foundry projects: Use full project endpoint URL

### Model Not Deployed

```
Error: "The deployment 'gpt-4o' could not be found"
```

**Solution**:

- Verify model is deployed in Azure AI Foundry portal
- Check deployment name matches environment variable
- Confirm deployment status is "Active"

### Quota Exceeded

```
Error: "Rate limit exceeded" or "Quota exceeded"
```

**Solution**:

- Check quota limits in Azure portal
- Request quota increase if needed
- Implement retry logic with exponential backoff

---

## Resources & Documentation

### Azure AI Foundry

- [Azure AI Foundry Portal](https://ai.azure.com)
- [Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [SDK Overview](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview)

### Authentication

- [DefaultAzureCredential](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme)
- [Azure Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/)

### Services

- [Azure AI Vision](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [DALL-E Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/dall-e-quickstart)

### Python SDKs

- [azure-ai-projects](https://pypi.org/project/azure-ai-projects/)
- [azure-identity](https://pypi.org/project/azure-identity/)
- [openai](https://pypi.org/project/openai/)

---

## Next Steps

1. **Review Individual PROJECT-UPGRADE.md** files for detailed guidance
2. **Start with Image Analysis and Face Detection** (no model deployments needed)
3. **Deploy models** for Gen AI Vision and DALL-E projects
4. **Test each project** with new authentication
5. **Commit changes** to version control
6. **Document** any custom configurations in project README

---

## Support & Questions

- Check individual PROJECT-UPGRADE.md files for project-specific issues
- Review [Troubleshooting](#troubleshooting-common-issues) section
- Consult Microsoft Learn documentation links
- Check Azure portal for service health and quotas

**Date Created**: December 14, 2025  
**Foundry Project Endpoint**: `https://pro-code-agents-resource.services.ai.azure.com/api/projects/pro-code-agents`
