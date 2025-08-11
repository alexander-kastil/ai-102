# Email Agent - Python Version

This is a Python implementation of the Semantic Kernel email agent that can send emails using Microsoft Graph API.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Copy the `.env` file and update it with your actual values:
   
   ```bash
   # Azure OpenAI Configuration
   SEMANTIC_KERNEL_MODEL=gpt-4o-mini
   SEMANTIC_KERNEL_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
   SEMANTIC_KERNEL_API_KEY=your-api-key-here

   # Microsoft Graph Configuration
   GRAPH_TENANT_ID=your-tenant-id
   GRAPH_CLIENT_ID=your-client-id
   GRAPH_CLIENT_SECRET=your-client-secret
   GRAPH_MAIL_SENDER=your-email@domain.com
   ```

## Usage

Run the email agent:
```bash
python main.py
```

The agent will start an interactive chat session where you can ask it to send emails. For example:
- "Send an email to john@example.com with subject 'Hello' and body 'How are you?'"
- "Email jane@company.com about the meeting tomorrow"

## Features

- **Semantic Kernel Integration**: Uses the latest Semantic Kernel Python SDK
- **Azure OpenAI**: Leverages GPT models for natural language understanding
- **Microsoft Graph**: Sends emails through Microsoft Graph API
- **Plugin Architecture**: Email functionality is implemented as a Semantic Kernel plugin
- **Environment Configuration**: Uses .env files for secure configuration management

## Project Structure

```
email-agent-py/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration (template)
├── common/
│   ├── __init__.py
│   ├── app_config.py      # Configuration management
│   └── graph_helper.py    # Microsoft Graph API integration
└── plugins/
    ├── __init__.py
    └── email_plugin.py    # Semantic Kernel email plugin
```

## Requirements

- Python 3.8+
- Azure OpenAI or OpenAI API access
- Microsoft Graph API permissions for sending emails
- Configured Azure AD application with appropriate permissions