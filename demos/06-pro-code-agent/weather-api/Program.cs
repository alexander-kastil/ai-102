var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};

app.MapPost("/weatherforecast", (WeatherRequest req) =>
{
    var random = new Random(req.City.GetHashCode() ^ req.Date.GetHashCode());
    var summary = summaries[random.Next(summaries.Length)];
    return new WeatherResult(req.City, summary, req.Date);
})
.WithName("GetWeatherForecast");

app.Run();

// Record types must be declared after all top-level statements
record WeatherRequest(string City, DateOnly Date);
record WeatherResult(string City, string Weather, DateOnly Date);
