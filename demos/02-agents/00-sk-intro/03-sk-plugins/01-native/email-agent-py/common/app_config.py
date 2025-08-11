"""Configuration management for the email agent."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class SemanticKernelConfig:
    """Configuration for Semantic Kernel."""
    model: str
    endpoint: str
    api_key: str


@dataclass
class GraphConfig:
    """Configuration for Microsoft Graph API."""
    tenant_id: str
    client_id: str
    client_secret: str
    mail_sender: str


@dataclass
class AppConfig:
    """Main application configuration."""
    semantic_kernel: SemanticKernelConfig
    graph: GraphConfig

    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create configuration from environment variables."""
        semantic_kernel = SemanticKernelConfig(
            model=os.getenv('SEMANTIC_KERNEL_MODEL', 'gpt-4o-mini'),
            endpoint=os.getenv('SEMANTIC_KERNEL_ENDPOINT', ''),
            api_key=os.getenv('SEMANTIC_KERNEL_API_KEY', '')
        )
        
        graph = GraphConfig(
            tenant_id=os.getenv('GRAPH_TENANT_ID', ''),
            client_id=os.getenv('GRAPH_CLIENT_ID', ''),
            client_secret=os.getenv('GRAPH_CLIENT_SECRET', ''),
            mail_sender=os.getenv('GRAPH_MAIL_SENDER', '')
        )
        
        return cls(semantic_kernel=semantic_kernel, graph=graph)