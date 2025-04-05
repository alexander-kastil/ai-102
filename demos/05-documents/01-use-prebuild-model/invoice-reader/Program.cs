using Azure;
using Azure.AI.FormRecognizer.DocumentAnalysis;
using Microsoft.Extensions.Configuration;

// Set up configuration
var configuration = new ConfigurationBuilder()
    .SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json")
    .Build();

// Read connection information from configuration
string? endpoint = configuration["FormRecognizer:Endpoint"];
string? apiKey = configuration["FormRecognizer:ApiKey"];

if (string.IsNullOrEmpty(endpoint) || string.IsNullOrEmpty(apiKey))
{
    throw new InvalidOperationException("Missing FormRecognizer:Endpoint or FormRecognizer:ApiKey in appsettings.json");
}

// Create the client
var cred = new AzureKeyCredential(apiKey);
var client = new DocumentAnalysisClient(new Uri(endpoint), cred);

Console.WriteLine("\nConnecting to Forms Recognizer at: {0}", endpoint);

const string invoicesFolder = "invoices";
const string searchPattern = "*.pdf";
foreach (string invoicePath in Directory.GetFiles(invoicesFolder, searchPattern))
{
    Console.WriteLine($"\nAnalyzing invoice: {invoicePath}\n");

    // Analyze the invoice using the local file
    using (var stream = File.OpenRead(invoicePath))
    {
        AnalyzeDocumentOperation operation = await client.AnalyzeDocumentAsync(WaitUntil.Completed, "prebuilt-invoice", stream);
        AnalyzeResult result = operation.Value;

        foreach (AnalyzedDocument invoice in result.Documents)
        {
            if (invoice.Fields.TryGetValue("VendorName", out DocumentField? vendorNameField))
            {
                if (vendorNameField.FieldType == DocumentFieldType.String)
                {
                    string vendorName = vendorNameField.Value.AsString();
                    Console.WriteLine($"Vendor Name: '{vendorName}', with confidence {vendorNameField.Confidence}.");
                }
            }

            if (invoice.Fields.TryGetValue("CustomerName", out DocumentField? customerNameField))
            {
                if (customerNameField.FieldType == DocumentFieldType.String)
                {
                    string customerName = customerNameField.Value.AsString();
                    Console.WriteLine($"Customer Name: '{customerName}', with confidence {customerNameField.Confidence}.");
                }
            }

            if (invoice.Fields.TryGetValue("InvoiceTotal", out DocumentField? invoiceTotalField))
            {
                if (invoiceTotalField.FieldType == DocumentFieldType.Currency)
                {
                    CurrencyValue invoiceTotal = invoiceTotalField.Value.AsCurrency();
                    Console.WriteLine($"Invoice Total: '{invoiceTotal.Symbol}{invoiceTotal.Amount}', with confidence {invoiceTotalField.Confidence}.");
                }
            }
        }
    }
    Console.WriteLine($"\nAnalysis of {Path.GetFileName(invoicePath)} complete.\n");
}