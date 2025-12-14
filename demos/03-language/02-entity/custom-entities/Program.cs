using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Azure;
using Azure.AI.Language.Text;
using Microsoft.Extensions.Configuration;

#nullable enable

namespace custom_entities
{
    internal static class Program
    {
        private const int BannerWidth = 80;

        private static void PrintBanner(string title)
        {
            Console.WriteLine();
            Console.WriteLine(new string('=', BannerWidth));
            Console.WriteLine(title);
            Console.WriteLine(new string('=', BannerWidth));
        }

        private static async Task RunAsync()
        {
            IConfigurationRoot configuration = new ConfigurationBuilder()
                .AddJsonFile("appsettings.json", optional: true)
                .Build();

            string? endpointValue = Environment.GetEnvironmentVariable("AI_SERVICE_ENDPOINT") ?? configuration["AIServicesEndpoint"];
            string? keyValue = Environment.GetEnvironmentVariable("AI_SERVICE_KEY") ?? configuration["AIServicesKey"];
            string? modelDeployment = Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME") ?? configuration["ModelDeployment"] ?? configuration["Deployment"];

            if (string.IsNullOrWhiteSpace(endpointValue) || string.IsNullOrWhiteSpace(keyValue))
            {
                throw new InvalidOperationException("Missing AI Service endpoint or key configuration.");
            }

            TextAnalysisClient client = new(new Uri(endpointValue), new AzureKeyCredential(keyValue));

            string adsPath = Path.Combine(AppContext.BaseDirectory, "ads");
            if (!Directory.Exists(adsPath))
            {
                throw new DirectoryNotFoundException($"Ads directory not found: {adsPath}");
            }

            foreach (string filePath in Directory.EnumerateFiles(adsPath, "*.txt").OrderBy(path => path))
            {
                string text = await File.ReadAllTextAsync(filePath).ConfigureAwait(false);
                if (string.IsNullOrWhiteSpace(text))
                {
                    continue;
                }

                PrintBanner($"Processing: {Path.GetFileName(filePath)}");

                MultiLanguageTextInput textInput = new()
                {
                    MultiLanguageInputs =
                    {
                        new MultiLanguageInput(Path.GetFileNameWithoutExtension(filePath), text.Trim())
                        {
                            Language = "en"
                        }
                    }
                };

                TextEntityRecognitionInput request = new()
                {
                    TextInput = textInput,
                    ActionContent = new EntitiesActionContent
                    {
                        ModelVersion = string.IsNullOrWhiteSpace(modelDeployment) ? "latest" : modelDeployment
                    }
                };

                var response = await client.AnalyzeTextAsync(request).ConfigureAwait(false);

                if (response.Value is AnalyzeTextEntitiesResult entitiesResult)
                {
                    foreach (EntityActionResult document in entitiesResult.Results.Documents)
                    {
                        foreach (NamedEntityWithMetadata entity in document.Entities)
                        {
                            Console.Write($"- {entity.Text} | {entity.Category}");
                            if (!string.IsNullOrWhiteSpace(entity.Subcategory))
                            {
                                Console.Write($"/{entity.Subcategory}");
                            }

                            Console.WriteLine($" | confidence={entity.ConfidenceScore}");
                        }
                    }

                    foreach (DocumentError error in entitiesResult.Results.Errors)
                    {
                        Console.WriteLine($"- Error in document {error.Id}: {error.Error.Code} - {error.Error.Message}");
                    }
                }
            }
        }

        private static async Task Main(string[] args)
        {
            try
            {
                await RunAsync().ConfigureAwait(false);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }
    }
}
