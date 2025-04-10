using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;

namespace FoodAppAI
{
    //To manage Migrations & create the DB go to console:
    //Add EF Core Tools: dotnet tool install --global dotnet-ef
    //dotnet restore
    //dotnet-ef migrations add MIGRATION-NAME
    //dotnet-ef database update

    public class FoodDBContext : DbContext //Use DbContext if not using Identity
    {
        public FoodDBContext(DbContextOptions<FoodDBContext> options) : base(options)
        {
            Database.EnsureCreated();
        }

        public DbSet<FoodItem> Food { get; set; }
        public DbSet<Drink> Drinks { get; set; }
        public DbSet<CartItem> CartItems { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            const string filePath = "fooditems.json";
            List<FoodItem> foodList = new List<FoodItem>();
            List<Drink> drinkList = new List<Drink>();

            if (File.Exists(filePath))
            {
                var jsonString = File.ReadAllText(filePath);
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                var data = JsonSerializer.Deserialize<FoodData>(jsonString, options);
                foodList = data?.Food ?? new List<FoodItem>();
                drinkList = data?.Drinks ?? new List<Drink>();
            }

            modelBuilder.Entity<FoodItem>().HasData(foodList.ToArray());
            modelBuilder.Entity<Drink>().HasData(drinkList.ToArray());
            modelBuilder.Entity<Drink>().HasKey(d => d.Id);


            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<CartItem>()
                .Property(c => c.Id)
                .ValueGeneratedOnAdd();
        }
    }

    public class FoodData
    {
        public List<FoodItem> Food { get; set; }
        public List<Drink> Drinks { get; set; }
    }
}