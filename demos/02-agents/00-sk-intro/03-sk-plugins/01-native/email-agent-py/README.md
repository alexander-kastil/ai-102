# Email Agent - Python Version

This is a Python port of the C# Semantic Kernel email agent sample with Microsoft Graph integration.

## Features

- Interactive chat interface with AI assistant
- Email sending capabilities (mock implementation for demo purposes)
- Function calling with Semantic Kernel plugins
- Approval workflow for consequential actions

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env`:
   - Semantic Kernel settings:
     - `DEPLOYMENT_MODEL`: Your AI model deployment name
     - `ENDPOINT`: Your Azure AI endpoint URL
     - `API_KEY`: Your Azure AI API key
   - Microsoft Graph settings (for demo purposes):
     - `TENANT_ID`: Your Azure AD tenant ID
     - `CLIENT_ID`: Your registered app client ID
     - `CLIENT_SECRET`: Your registered app client secret
     - `MAIL_SENDER`: The email address to send from

## Usage

```bash
python main.py
```

The agent will start an interactive chat session where you can ask it to send emails. It will:
1. Ask for clarification if needed
2. Request approval before sending emails
3. Use a mock implementation to demonstrate email sending workflow

## Note

This demo uses a mock email implementation. For production use, you would need to:
1. Install the full Microsoft Graph SDK: `pip install msgraph-sdk`
2. Register an Azure AD application with appropriate Microsoft Graph permissions
3. Replace the mock `GraphHelper` with the actual Graph SDK implementation