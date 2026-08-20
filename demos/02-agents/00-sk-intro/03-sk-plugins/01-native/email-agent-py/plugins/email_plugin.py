"""Email plugin for Semantic Kernel."""

from typing import List, Annotated
from semantic_kernel.functions import kernel_function
from semantic_kernel.kernel import Kernel

from ..common.app_config import GraphConfig
from ..common.graph_helper import GraphHelper


class EmailPlugin:
    """Plugin for sending emails using Semantic Kernel."""

    def __init__(self, config: GraphConfig):
        """Initialize the EmailPlugin with Graph configuration."""
        self.config = config

    @kernel_function(
        description="Sends an email to recipients",
        name="send_email",
    )
    async def send_email(
        self,
        recipient_emails: Annotated[List[str], "List of recipient email addresses"],
        subject: Annotated[str, "Email subject"],
        body: Annotated[str, "Email body content"],
    ) -> str:
        """Send an email to the specified recipients."""
        print(f"Sending email to recipients: {', '.join(recipient_emails)}")
        
        try:
            graph_helper = GraphHelper(self.config)
            await graph_helper.send_mail(subject, body, recipient_emails)
            return f"Email sent successfully to {', '.join(recipient_emails)}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"