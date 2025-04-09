namespace FoodAppAI
{
    public class FoodItem
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public decimal Price { get; set; }
        public int InStock { get; set; }
        public string PictureUrl { get; set; }
        public List<string> Allergies { get; set; }
        public List<string> Diet { get; set; }
        public int Calories { get; set; }
    }
}