from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Store connection information
endpoint = os.getenv('AZURE_ENDPOINT')
key = os.getenv('AZURE_API_KEY')

# Constants
fileLocale = "en-US"
fileModelId = "prebuilt-invoice"

print(f"\nConnecting to Forms Recognizer at: {endpoint}")

# Create the client
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Process all files in the invoices folder
invoice_folder = "invoices"
for filename in os.listdir(invoice_folder):
    if filename.endswith('.pdf'):
        file_path = os.path.join(invoice_folder, filename)
        
        print(f"\nAnalyzing invoice: {filename}")
        
        # Open the file and analyze the invoice
        with open(file_path, "rb") as f:
            poller = document_analysis_client.begin_analyze_document(
                fileModelId, 
                document=f,
                locale=fileLocale
            )
            receipts = poller.result()

        # Display invoice information to the user
        for receipt in receipts.documents:
            vendor_name = receipt.fields.get("VendorName")
            if vendor_name:
                print(f"Vendor Name: {vendor_name.value}, with confidence {vendor_name.confidence:.2f}")

            customer_name = receipt.fields.get("CustomerName")
            if customer_name:
                print(f"Customer Name: {customer_name.value}, with confidence {customer_name.confidence:.2f}")

            invoice_total = receipt.fields.get("InvoiceTotal")
            if invoice_total:
                print(f"Invoice Total: {invoice_total.value.symbol}{invoice_total.value.amount}, with confidence {invoice_total.confidence:.2f}")

print("\nAnalysis complete.\n")