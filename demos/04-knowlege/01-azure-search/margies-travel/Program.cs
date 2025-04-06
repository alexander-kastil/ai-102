using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorPages();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}
else
{
    app.UseDeveloperExceptionPage();
}

app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

// Add redirect rule for index.html
app.Use(async (context, next) =>
{
    if (context.Request.Path.Value?.Equals("/index.html", StringComparison.OrdinalIgnoreCase) == true)
    {
        context.Response.Redirect("/");
        return;
    }
    await next();
});

app.MapRazorPages();

app.Run();
