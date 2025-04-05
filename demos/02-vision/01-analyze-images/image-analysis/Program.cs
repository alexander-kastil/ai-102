using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Drawing;
using Microsoft.Extensions.Configuration;
using Azure;
using Azure.AI.Vision.ImageAnalysis;

namespace image_analysis
{
    class Program
    {
        static async Task Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string aiSvcEndpoint = configuration["AIServicesEndpoint"];
                string aiSvcKey = configuration["AIServicesKey"];

                // Get image
                string imageFile = "images/street.jpg";
                if (args.Length > 0)
                {
                    imageFile = args[0];
                }

                // Create client with Azure AI Services credentials
                ImageAnalysisClient client = new(
                    new Uri(aiSvcEndpoint),
                    new AzureKeyCredential(aiSvcKey));

                // Analyze image
                await AnalyzeImage(imageFile, client);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task AnalyzeImage(string imageFile, ImageAnalysisClient client)
        {
            Console.WriteLine($"\nAnalyzing {imageFile} \n");

            // Use BinaryData to pass the image data
            BinaryData imageData = await BinaryData.FromStreamAsync(File.OpenRead(imageFile));

            // Get result with specified features to be retrieved
            var features = VisualFeatures.Caption |
                         VisualFeatures.DenseCaptions |
                         VisualFeatures.Objects |
                         VisualFeatures.People |
                         VisualFeatures.Read |
                         VisualFeatures.Tags;

            var result = await client.AnalyzeAsync(imageData, features);

            // Display analysis results
            if (result.Value.Caption != null)
            {
                Console.WriteLine($" Caption: '{result.Value.Caption.Text}' (confidence: {result.Value.Caption.Confidence:0.0000})");
            }

            if (result.Value.DenseCaptions != null)
            {
                Console.WriteLine($" Dense Captions: {result.Value.DenseCaptions.Values.Count}");
                foreach (var caption in result.Value.DenseCaptions.Values)
                {
                    Console.WriteLine($"  '{caption.Text}' (confidence: {caption.Confidence:0.0000})");
                }
            }

            if (result.Value.Objects != null)
            {
                Console.WriteLine($" Objects: {result.Value.Objects.Values.Count}");
                foreach (var obj in result.Value.Objects.Values)
                {
                    var tag = obj.Tags.Count > 0 ? obj.Tags[0].Name : "Unknown";
                    Console.WriteLine($"  '{tag}'");
                }
            }

            if (result.Value.Tags != null)
            {
                Console.WriteLine($" Tags: {result.Value.Tags.Values.Count}");
                foreach (var tag in result.Value.Tags.Values)
                {
                    Console.WriteLine($"  '{tag.Name}' (confidence: {tag.Confidence:0.0000})");
                }
            }
        }
    }
}
