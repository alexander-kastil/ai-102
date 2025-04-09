using System.ComponentModel;
using Microsoft.SemanticKernel;

namespace FoodAppAI
{
    [Description("A plugin to manage shopping cart items")]
    public class ShoppingCartPlugin(FoodDBContext ctx)
    {
        [KernelFunction, Description("Add a food menu or drink to the shopping cart. Take the price of the item from the corresponding FoodItem or Drink. Valid messages are: I take 2 of the burger, Add 3 of the coke to my cart, Water would be fine, etc.")]
        public void AddToCart(
            [Description("Cart item details")] CartItem item,
            [Description("Amount of the item")] int amount)
        {
            item.Amount = amount;
            ctx.CartItems.Add(item);
            ctx.SaveChanges();
        }

        [KernelFunction, Description("Remove a food menu or drink from the shopping cart based on the username.  Valid messages are: Remove all burgers, Delete 2 cokes, Clear the cart.")]
        public void RemoveFromCart(
            [Description("Item ID")] int itemId,
            [Description("Type of the item (FoodItem or Drink)")] string type)
        {
            var cartItem = ctx.CartItems.FirstOrDefault(ci => ci.ItemId == itemId && ci.Type == type);
            if (cartItem != null)
            {
                ctx.CartItems.Remove(cartItem);
                ctx.SaveChanges();
            }
        }

        [KernelFunction, Description("Get the current state of the cart for a user. Valid messages are: What to i have, What is the total, Get my cart.")]
        public List<CartItem> GetCartState()
        {
            var cartItems = ctx.CartItems.ToList();
            Console.WriteLine("Cart items: " + cartItems.Count);
            return cartItems;
        }
    }
}