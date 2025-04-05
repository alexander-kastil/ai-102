using System.ClientModel;
using Microsoft.Extensions.Configuration;
using Azure.AI.OpenAI;
using OpenAI.Chat;

// Build a config object and retrieve user settings.
class ChatMessageLab
{

    static string? oaiEndpoint;
    static string? oaiKey;
    static string? oaiDeploymentName;
    static void Main(string[] args)
    {
        IConfiguration config = new ConfigurationBuilder()
            .AddJsonFile("appsettings.json")
            .Build();

        oaiEndpoint = config["AzureOAIEndpoint"];
        oaiKey = config["AzureOAIKey"];
        oaiDeploymentName = config["AzureOAIDeploymentName"];

        // Read system message once at startup
        string systemMessage = System.IO.File.ReadAllText("data/system.txt").Trim();

        do
        {
            Console.WriteLine("\nEnter your prompt or type 'quit' to exit:");
            string userMessage = Console.ReadLine()?.Trim() ?? "";

            if (userMessage.ToLower() == "quit")
            {
                break;
            }
            else if (string.IsNullOrEmpty(userMessage))
            {
                Console.WriteLine("Please enter a prompt.");
                continue;
            }
            else
            {
                GetResponseFromOpenAI(systemMessage, userMessage);
            }
        } while (true);

    }

    private static void GetResponseFromOpenAI(string systemMessage, string userMessage)
    {
        Console.WriteLine("\nSending prompt to Azure OpenAI endpoint...\n\n");

        if (string.IsNullOrEmpty(oaiEndpoint) || string.IsNullOrEmpty(oaiKey) || string.IsNullOrEmpty(oaiDeploymentName))
        {
            Console.WriteLine("Please check your appsettings.json file for missing or incorrect values.");
            return;
        }

        // Configure the Azure OpenAI client
        AzureOpenAIClient azureClient = new(new Uri(oaiEndpoint), new ApiKeyCredential(oaiKey));
        ChatClient chatClient = azureClient.GetChatClient(oaiDeploymentName);

        // Get response from Azure OpenAI
        ChatCompletionOptions chatCompletionOptions = new ChatCompletionOptions()
        {
            Temperature = 0.7f,
            MaxOutputTokenCount = 800
        };

        ChatCompletion completion = chatClient.CompleteChat(
            [
                new SystemChatMessage(systemMessage),
            new UserChatMessage(userMessage)
            ],
            chatCompletionOptions
        );

        Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
    }
}