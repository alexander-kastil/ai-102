# Semantic Kernel Python Conversions

This folder contains Python versions of all the C# Semantic Kernel samples, with the "-py" suffix as requested.

## Converted Samples

### 1. Chat Completion (`sk-chat-completion-py`)
- **Original**: `01-sk-chat-completion/sk-chat-completion`
- **Python**: `01-sk-chat-completion/sk-chat-completion-py`
- **Features**: Basic chat completion with multimodal image processing

### 2. Email Agent (`email-agent-py`) 
- **Original**: `03-sk-plugins/01-native/email-agent`
- **Python**: `03-sk-plugins/01-native/email-agent-py`
- **Features**: Interactive chat with email sending plugin (mock implementation)

### 3. MCP GitHub Agent (`sk-use-mcp-py`)
- **Original**: `03-sk-plugins/02-mcp/sk-use-mcp` 
- **Python**: `03-sk-plugins/02-mcp/sk-use-mcp-py`
- **Features**: Model Context Protocol integration with GitHub tools simulation

### 4. RAG Student App (`sk-students-ai-py`)
- **Original**: `03-sk-rag/sk-students-ai`
- **Python**: `03-sk-rag/sk-students-ai-py` 
- **Features**: Flask web application with RAG functionality for student Q&A

## Common Features

All Python samples include:
- ✅ Azure AI Inference connector for stability
- ✅ Proper error handling and user feedback  
- ✅ Environment variable configuration via .env files
- ✅ Requirements.txt for dependency management
- ✅ Comprehensive README files with setup instructions
- ✅ Functional equivalence to original C# versions

## Quick Start

For any sample:
1. Navigate to the `-py` folder
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` file with your Azure AI credentials
4. Run: `python main.py` (or `python app.py` for the web app)

## Technical Notes

- Uses Azure AI Inference instead of direct OpenAI connector for better compatibility
- FunctionChoiceBehavior replaces deprecated FunctionCallBehavior
- Mock implementations provided where external services are complex to set up
- All samples tested for proper imports and basic functionality