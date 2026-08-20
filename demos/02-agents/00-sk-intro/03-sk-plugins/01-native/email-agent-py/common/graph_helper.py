"""Microsoft Graph helper for sending emails."""

from typing import List
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import SendMailPostRequestBody

from .app_config import GraphConfig


class GraphHelper:
    """Helper class for Microsoft Graph operations."""

    def __init__(self, config: GraphConfig):
        """Initialize the GraphHelper with configuration."""
        self.config = config
        
        # Create credentials
        credential = ClientSecretCredential(
            tenant_id=config.tenant_id,
            client_id=config.client_id,
            client_secret=config.client_secret
        )
        
        # Create Graph client
        self.graph_client = GraphServiceClient(
            credentials=credential,
            scopes=['https://graph.microsoft.com/.default']
        )

    async def send_mail(self, subject: str, message: str, recipients: List[str]) -> None:
        """Send an email using Microsoft Graph API."""
        # Create recipient list
        recipient_list = []
        for recipient_email in recipients:
            email_address = EmailAddress()
            email_address.address = recipient_email
            
            recipient = Recipient()
            recipient.email_address = email_address
            
            recipient_list.append(recipient)

        # Create message body
        body = ItemBody()
        body.content_type = BodyType.Html
        body.content = message

        # Create email message
        email_message = Message()
        email_message.subject = subject
        email_message.body = body
        email_message.to_recipients = recipient_list

        # Send the email
        await self._send_mail_using_graph(email_message)

    async def _send_mail_using_graph(self, message: Message) -> None:
        """Send email message using Graph API."""
        request_body = SendMailPostRequestBody()
        request_body.message = message
        request_body.save_to_sent_items = False

        await self.graph_client.users.by_user_id(self.config.mail_sender).send_mail.post(request_body)