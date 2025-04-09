using FoodAppAI;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;

var builder = new ConfigurationBuilder()
    .SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

IConfiguration configuration = builder.Build();

var cs = configuration["ConnectionStrings:DefaultConnection"];
var model = configuration["SemanticKernel:DeploymentModel"];
var endpoint = configuration["SemanticKernel:Endpoint"];
var resourceKey = configuration["SemanticKernel:ApiKey"];

var kernelBuilder = Kernel.CreateBuilder();

kernelBuilder.Services.AddDbContext<FoodDBContext>(options => options.UseSqlite(cs));

// register plugins - native functions
kernelBuilder.Plugins.AddFromType<RestaurantPlugin>();
kernelBuilder.Plugins.AddFromType<ShoppingCartPlugin>();

PromptExecutionSettings settings = new PromptExecutionSettings()
{
    FunctionChoiceBehavior = FunctionChoiceBehavior.Auto()
};

kernelBuilder.Services.AddAzureOpenAIChatCompletion(
    model,
    endpoint,
    resourceKey
);

kernelBuilder.Services.AddLogging(loggingBuilder =>
{
    loggingBuilder.AddConsole();
});

var kernel = kernelBuilder.Build();

// register semantic functions
string skPrompt = @"Create a description that could be used to describe a dish in a restaurant. The description should include the name of the dish, the ingredients, and the preparation method. The description should be 3-4 sentences long. Dish to describe: {{$userInput}}. Do not include preparation instructions";

var function = kernel.CreateFunctionFromPrompt(
    promptTemplate: skPrompt,
    functionName: "DescribeDish"
);

Console.WriteLine("Good day. What is your name?");
string username = Console.ReadLine();
Console.WriteLine($"Hello {username}! How can I help you? Do you have anything special in mind?");

while (true)
{
    var userInput = Console.ReadLine();
    if (string.IsNullOrEmpty(userInput)) continue;

    if (userInput.ToLower().Contains("checkout"))
    {
        Console.WriteLine("Thank you for visiting! Have a great day!");
        break;
    }

    var result = await kernel.InvokePromptAsync(userInput, new KernelArguments(settings));
    Console.WriteLine(result);
}