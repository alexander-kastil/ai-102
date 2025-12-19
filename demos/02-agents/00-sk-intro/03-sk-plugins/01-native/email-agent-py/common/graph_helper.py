from typing import List
from common.config import GraphConfig

class GraphHelper:
    def __init__(self, config: GraphConfig):
        self.config = config
        print(f"Initialized Graph Helper for tenant: {config.tenant_id}")
    
    async def send_mail(self, subject: str, message: str, recipients: List[str]):
        """Send email using Microsoft Graph API (mock implementation)"""
        print(f"[MOCK] Sending email:")
        print(f"  From: {self.config.mail_sender}")
        print(f"  To: {', '.join(recipients)}")
        print(f"  Subject: {subject}")
        print(f"  Body: {message}")
        
        # In a real implementation, this would use the Microsoft Graph SDK
        # to send the actual email. For demo purposes, we're just logging.
        
        return True