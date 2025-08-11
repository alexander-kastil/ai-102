# Semantic Kernel Chat Completion - Python Version

This is a Python port of the C# Semantic Kernel chat completion sample.

## Features

- Basic chat completion using Azure AI Inference
- Multimodal capabilities (text + image processing)
- Streaming and non-streaming response handling
- Environment variable configuration

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env`:
   - `DEPLOYMENT_MODEL`: Your AI model deployment name (e.g., "gpt-4o-mini")
   - `ENDPOINT`: Your Azure AI endpoint URL
   - `API_KEY`: Your Azure AI API key

## Usage

```bash
python main.py
```

The sample will:
1. Generate a poem about whippets and the sea
2. Analyze the provided image (data/soi-beach.jpg) using multimodal capabilities

## Note

This Python version uses Azure AI Inference connector for better compatibility and reliability compared to the direct OpenAI connector.