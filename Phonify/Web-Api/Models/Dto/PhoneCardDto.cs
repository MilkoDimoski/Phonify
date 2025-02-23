namespace Phonify.Models.Dto
{
    public class PhoneCardDto
    {
        public string Brand { get; set; } // Brand of the phone
        public string Model { get; set; } // Model of the phone
        public List<string> WholeNames { get; set; } // Variations of the model
        public decimal CheapestPrice { get; set; } // Lowest price for the model
        public int OfferCount { get; set; } // Total offers for the model
    }
}
