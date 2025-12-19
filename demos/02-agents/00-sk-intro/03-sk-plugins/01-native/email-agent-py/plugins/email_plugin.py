from typing import List
from semantic_kernel.functions import kernel_function
from common.graph_helper import GraphHelper
from common.config import GraphConfig

class EmailPlugin:
    def __init__(self, graph_config: GraphConfig):
        self.graph_helper = GraphHelper(graph_config)
    
    @kernel_function(
        name="send_email",
        description="Sends an email to a recipient."
    )
    async def send_email(
        self,
        recipient_emails: List[str],
        subject: str,
        body: str
    ) -> str:
        """Send an email to the specified recipients."""
        try:
            print(f"Sending email to recipients: {', '.join(recipient_emails)}")
            await self.graph_helper.send_mail(subject, body, recipient_emails)
            return f"Email sent successfully to {', '.join(recipient_emails)}"
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            print(error_msg)
            return error_msg