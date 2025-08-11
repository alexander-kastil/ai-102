from typing import List
from azure.identity import ClientSecretCredential
from microsoft.graph import GraphServiceClient
from common.config import GraphConfig

class GraphHelper:
    def __init__(self, config: GraphConfig):
        self.config = config
        
        credentials = ClientSecretCredential(
            tenant_id=config.tenant_id,
            client_id=config.client_id,
            client_secret=config.client_secret
        )
        
        self.graph_client = GraphServiceClient(
            credentials=credentials,
            scopes=["https://graph.microsoft.com/.default"]
        )
    
    async def send_mail(self, subject: str, message: str, recipients: List[str]):
        """Send email using Microsoft Graph API"""
        recipient_list = []
        
        for recipient in recipients:
            recipient_list.append({
                "emailAddress": {
                    "address": recipient
                }
            })
        
        email_message = {
            "subject": subject,
            "body": {
                "contentType": "html",
                "content": message
            },
            "toRecipients": recipient_list
        }
        
        request_body = {
            "message": email_message,
            "saveToSentItems": False
        }
        
        try:
            await self.graph_client.users.by_user_id(self.config.mail_sender).send_mail.post(
                body=request_body
            )
            print(f"Email sent successfully to: {', '.join(recipients)}")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            raise