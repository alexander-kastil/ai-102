# Model Context Protocol Sample - Python

This example demonstrates how to use Model Context Protocol tools with Semantic Kernel in Python.

MCP is an open protocol that standardizes how applications provide context to LLMs.

For information on Model Context Protocol (MCP) please refer to the [documentation](https://modelcontextprotocol.io/introduction).

The sample shows:

1. How to connect to an MCP Server using the Python `mcp` package
2. Retrieve the list of tools the MCP Server makes available
3. Convert the MCP tools to Semantic Kernel functions so they can be added to a Kernel instance
4. Invoke the tools from Semantic Kernel using function calling
5. Create an Azure AI Agent that can use the MCP tools

## Installing Prerequisites

The sample requires node.js and npm to be installed. So, please install them from [here](https://nodejs.org/en/download/).

## Python Environment Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuring Environment Variables

The example requires credentials to access Azure OpenAI. Create a `.env` file in this directory with the following variables:

```env
MODEL="gpt-4o"
API_KEY="your-azure-openai-api-key"
ENDPOINT="https://your-resource.cognitiveservices.azure.com"
GIT_REPO="username/repository-name"
```

Example:
```env
MODEL="gpt-4o"
API_KEY="31O4sG4UtDQQpnCcnwFS9guSccBhDzk8JFzzphQ6TFHI17NgtehYJQQJ99BHACYeBjFXJ3w3AAAAACOGNjob"
ENDPOINT="https://ai-102-foundry-resource.cognitiveservices.azure.com"
GIT_REPO="alexander-kastil/github-copilot-skills-fest"
```

## Running the Sample

### Option 1: Test connectivity first (Recommended)

```bash
python test_mcp.py
```

This will test:
- Configuration loading from .env file
- Node.js/npx availability  
- MCP GitHub server accessibility

### Option 2: Run the basic demo

```bash
python main.py
```

This shows the structure and demonstrates the concept without requiring all dependencies.

### Option 3: Run the full implementation

```bash
pip install -r requirements.txt
python main_full.py
```

This requires all dependencies to be installed and provides the complete functionality.

## What the Sample Does

1. **MCP Client Creation**: Creates an MCP client that connects to the GitHub server via npx
2. **Tool Discovery**: Lists all available tools from the GitHub MCP server
3. **Kernel Setup**: Creates a Semantic Kernel with Azure OpenAI chat completion
4. **Plugin Creation**: Converts MCP tools to a Semantic Kernel plugin
5. **Direct Testing**: Tests the kernel with GitHub queries
6. **Agent Creation**: Creates an Azure AI Agent with the GitHub plugin
7. **Interactive Testing**: Tests various GitHub-related queries through the agent

## Files in this Directory

- `main.py` - Basic demo showing the structure (minimal dependencies)
- `main_full.py` - Complete implementation (requires all dependencies)  
- `test_mcp.py` - Connectivity and configuration test
- `requirements.txt` - Python package dependencies
- `.env` - Configuration file (Azure OpenAI credentials, etc.)
- `README.md` - This documentation

## Key Differences from C# Version

- Uses `.env` file instead of `appsettings.json` for configuration
- Uses Python `mcp` package instead of .NET ModelContextProtocol package
- Uses Python Semantic Kernel SDK
- Uses `python-dotenv` for environment variable loading
- Async/await pattern consistent with Python asyncio

## Troubleshooting

- Make sure Node.js and npm are installed
- Ensure the MCP GitHub server can be installed: `npx -y @modelcontextprotocol/server-github`
- Check that your Azure OpenAI credentials are correct
- Verify the repository name exists and is accessible