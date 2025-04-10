using System.ComponentModel;
using Microsoft.SemanticKernel;

namespace FoodAppAI
{
    [Description("A plugin to manage food menus and drinks for a restaurant")]
    public class RestaurantPlugin(FoodDBContext ctx)
    {
        [KernelFunction, Description("Get all food menu items including diet recommendations, allergies, calories and prices")]
        public List<FoodItem> GetMenuItems()
        {
            return ctx.Food.ToList();
        }

        [KernelFunction, Description("Filter food items by allergies and/or diet preferences. Valid messages are: I am allergic to gluten, What Keto do you have, I am on low carb, I am vegan, I am allergic to gluten and vegan, etc.")]
        public List<FoodItem> FilterFoodItems(
            [Description("Comma-separated list of allergies to exclude (e.g., 'gluten, shellfish, dairy')")] string allergies,
            [Description("Comma-separated list of dietary preferences to include (e.g., 'vegetarian, vegan, low carb, keto')")] string diet)
        {
            var query = ctx.Food.AsQueryable();

            if (!string.IsNullOrEmpty(allergies))
            {
                string[] allergyList = allergies.Split(',', StringSplitOptions.TrimEntries)
                    .Select(a => a.ToLower())
                    .ToArray();
                query = query.Where(f => !f.Allergies.Any(a => allergyList.Contains(a.ToLower())));
            }

            if (!string.IsNullOrEmpty(diet))
            {
                string[] dietList = diet.Split(',', StringSplitOptions.TrimEntries)
                    .Select(d => d.ToLower())
                    .ToArray();
                query = query.Where(f => f.Diet.Any(d => dietList.Contains(d.ToLower())));
            }

            var result = query.ToList();
            return result;
        }

        [KernelFunction, Description("Find a specific food or drink by its name to get its details for the cart. Valid messages are: How much is the Wiener Schnitzel, What is the price of coke, Tell me about the salad")]
        public CartItem GetItemByName(
            [Description("Name of the food or drink item to find")] string name)
        {
            var food = ctx.Food.FirstOrDefault(f => f.Name.ToLower().Contains(name.ToLower()));
            if (food != null)
            {
                return new CartItem
                {
                    ItemId = food.Id,
                    ItemName = food.Name,
                    Price = food.Price,
                    Type = "FoodItem"
                };
            }

            var drink = ctx.Drinks.FirstOrDefault(d => d.Name.ToLower() == name.ToLower());
            if (drink != null)
            {
                return new CartItem
                {
                    ItemId = drink.Id,
                    ItemName = drink.Name,
                    Price = drink.Price,
                    Type = "Drink"
                };
            }

            return null;
        }

        [KernelFunction, Description("Get all drink menu items with prices and calories")]
        public List<Drink> GetDrinkItems()
        {
            return ctx.Drinks.ToList();
        }

    }
}