import os
from dataclasses import dataclass
from typing import List

@dataclass
class GraphConfig:
    tenant_id: str
    client_id: str
    client_secret: str
    graph_api_uri: str
    return_url: str
    mail_sender: str

@dataclass  
class AppConfig:
    deployment_model: str
    endpoint: str
    api_key: str
    graph_config: GraphConfig
    
    @classmethod
    def from_env(cls):
        graph_config = GraphConfig(
            tenant_id=os.getenv("TENANT_ID"),
            client_id=os.getenv("CLIENT_ID"), 
            client_secret=os.getenv("CLIENT_SECRET"),
            graph_api_uri=os.getenv("GRAPH_API_URI", "https://graph.microsoft.com"),
            return_url=os.getenv("RETURN_URL", "https://localhost:5001/"),
            mail_sender=os.getenv("MAIL_SENDER")
        )
        
        return cls(
            deployment_model=os.getenv("DEPLOYMENT_MODEL"),
            endpoint=os.getenv("ENDPOINT"),
            api_key=os.getenv("API_KEY"),
            graph_config=graph_config
        )