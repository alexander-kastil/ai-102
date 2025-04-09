namespace FoodAppAI
{
    public class CartItem
    {
        public int Id { get; set; }
        public int ItemId { get; set; }
        public string ItemName { get; set; }
        public decimal Price { get; set; }
        public int Amount { get; set; }
        public string Type { get; set; }
    }
}