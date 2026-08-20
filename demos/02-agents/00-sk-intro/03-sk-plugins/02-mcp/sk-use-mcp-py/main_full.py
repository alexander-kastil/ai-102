"""
Model Context Protocol Sample with Semantic Kernel in Python - Full Implementation

This is the complete implementation that requires all dependencies to be installed.
"""

import asyncio
import os
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List

# These imports require pip install -r requirements.txt
try:
    from dotenv import load_dotenv
    from mcp import McpClient, StdioClientTransport
    from azure.identity.aio import DefaultAzureCredential
    from semantic_kernel import Kernel
    from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings
    from semantic_kernel.connectors.ai.azure_ai import AzureAIChatCompletion
    from semantic_kernel.functions import KernelFunction
    from semantic_kernel.functions.kernel_function_decorator import kernel_function
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Dependencies not available: {e}")
    print("Please run: pip install -r requirements.txt")
    DEPENDENCIES_AVAILABLE = False


def load_env_config():
    """Load configuration from .env file."""
    if DEPENDENCIES_AVAILABLE:
        load_dotenv()
        return {
            "MODEL": os.getenv("MODEL"),
            "ENDPOINT": os.getenv("ENDPOINT"),
            "API_KEY": os.getenv("API_KEY"),
            "GIT_REPO": os.getenv("GIT_REPO")
        }
    else:
        # Fallback to manual parsing
        env_path = Path(__file__).parent / '.env'
        config = {}
        
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip().strip('"\'')
        
        return config


async def main():
    """Main function that replicates the C# Program.cs functionality."""
    
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Load configuration
    config = load_env_config()
    
    model = config.get("MODEL")
    endpoint = config.get("ENDPOINT") 
    api_key = config.get("API_KEY")
    git_repo = config.get("GIT_REPO")
    
    if not all([model, endpoint, api_key, git_repo]):
        raise ValueError("Missing required configuration. Check your .env file.")
    
    print(f"Configuration loaded:")
    print(f"Model: {model}")
    print(f"Endpoint: {endpoint}")
    print(f"Repository: {git_repo}")
    print()

    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Dependencies not installed. Please run:")
        print("   pip install -r requirements.txt")
        return

    try:
        # Create an MCP Client for the GitHub server
        print("Creating MCP client for GitHub server...")
        mcp_client = await create_mcp_client()
        
        # Retrieve the list of tools available on the GitHub server
        print("Retrieving available tools from MCP server...")
        tools = await mcp_client.list_tools()
        
        print("Available tools:")
        for tool in tools:
            print(f"  {tool.name}: {tool.description}")
        print()
        
        # Create and configure Semantic Kernel
        print("Setting up Semantic Kernel...")
        kernel = await create_semantic_kernel(model, endpoint, api_key)
        
        # Add MCP tools as Kernel functions
        print("Converting MCP tools to Kernel functions...")
        github_plugin = await create_github_plugin_from_mcp_tools(tools, mcp_client)
        kernel.add_plugin(github_plugin, plugin_name="GitHub")
        
        # Test using GitHub tools directly with Kernel
        print("\n" + "="*50)
        print("TESTING KERNEL WITH GITHUB TOOLS")
        print("="*50)
        
        prompt = f"Summarize the last commit to the {git_repo} repository?"
        print(f"\nPrompt: {prompt}")
        
        response = await kernel.invoke_prompt(
            prompt, 
            template_format="semantic-kernel",
            settings={
                "max_tokens": 1000,
                "temperature": 0.0
            }
        )
        print(f"Response: {response}")
        
        # Create an Azure AI Agent with MCP tools
        print("\n" + "="*50) 
        print("TESTING WITH AZURE AI AGENT")
        print("="*50)
        
        # Get Azure AI Agent settings
        ai_agent_settings = AzureAIAgentSettings()
        
        async with DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        ) as creds:
            
            async with AzureAIAgent.create_client(credential=creds) as client:
                
                # Create the GitHub agent
                agent_definition = await client.agents.create_agent(
                    model=model,
                    name="GitHubAgent",
                    instructions="Answer questions about GitHub repositories using the available GitHub tools."
                )
                
                github_agent = AzureAIAgent(
                    client=client,
                    definition=agent_definition,
                    plugins=[github_plugin]
                )
                
                # Test various prompts that match the C# version
                test_prompts = [
                    f"Summarize the last commit to the {git_repo} repository?",
                    f"Summarize the latest commit in the {git_repo} repository?", 
                    f"Summarize the last issue in the {git_repo} repository?"
                ]
                
                for prompt in test_prompts:
                    print(f"\nPrompt: {prompt}")
                    response = await github_agent.get_response([prompt])
                    print(f"GitHubAgent Response: {response}")
                    print("-" * 40)
                
                # Cleanup
                await client.agents.delete_agent(github_agent.id)
                print("\nAgent cleaned up successfully.")
        
        # Close MCP client
        await mcp_client.close()
        print("MCP client closed.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def create_mcp_client():
    """Create and initialize an MCP client for the GitHub server."""
    
    # Create stdio transport for npx @modelcontextprotocol/server-github
    transport = StdioClientTransport(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"]
    )
    
    # Create and initialize MCP client
    mcp_client = McpClient(transport)
    await mcp_client.initialize()
    
    return mcp_client


async def create_semantic_kernel(model: str, endpoint: str, api_key: str) -> Kernel:
    """Create and configure a Semantic Kernel instance."""
    
    kernel = Kernel()
    
    # Add Azure OpenAI chat completion
    kernel.add_service(AzureAIChatCompletion(
        deployment_name=model,
        endpoint=endpoint,
        api_key=api_key,
        service_id="azure_openai_chat"
    ))
    
    return kernel


async def create_github_plugin_from_mcp_tools(tools: List[Any], mcp_client) -> object:
    """Convert MCP tools to a Semantic Kernel plugin."""
    
    class GitHubPlugin:
        """A plugin that wraps MCP GitHub tools."""
        
        def __init__(self, mcp_client):
            self.mcp_client = mcp_client
            self.tools_map = {tool.name: tool for tool in tools}
        
        async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
            """Call an MCP tool and return the result."""
            try:
                result = await self.mcp_client.call_tool(tool_name, arguments)
                return str(result.content) if hasattr(result, 'content') else str(result)
            except Exception as e:
                return f"Error calling {tool_name}: {str(e)}"
    
    plugin = GitHubPlugin(mcp_client)
    
    # Dynamically add methods for each MCP tool
    for tool in tools:
        tool_name = tool.name
        tool_description = tool.description
        
        # Create a wrapper function for this specific tool
        def make_tool_function(name: str):
            async def tool_func(self, **kwargs) -> str:
                return await self.call_mcp_tool(name, kwargs)
            return tool_func
        
        # Add the function to the plugin with proper decorator
        func = make_tool_function(tool_name)
        func.__name__ = tool_name.replace('-', '_')  # Make valid Python identifier
        func = kernel_function(description=tool_description)(func)
        setattr(plugin, func.__name__, func.__get__(plugin, GitHubPlugin))
    
    return plugin


if __name__ == "__main__":
    asyncio.run(main())