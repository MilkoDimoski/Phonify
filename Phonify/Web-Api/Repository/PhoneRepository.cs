using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Phonify.Models;
using Phonify.Models.Dto;

namespace Phonify.Repository
{
    public class PhoneRepository : IPhoneRepository
    {
        private readonly PhoneContext _context;
        public PhoneRepository(PhoneContext context)
        {
            this._context = context;

        }
        public async Task<Phone> GetPhoneAsync(int id)
        {
            return await _context.Mobile.FindAsync(id);

        }
       

        public async Task<List<Phone>> GetAllPhonesAsync()
        {
            return await _context.Mobile.ToListAsync();
        }

        public async Task<List<string>> GetDistinctBrandsAsync()
        {
            return await _context.Mobile.Select(p => p.Brand).Distinct().ToListAsync();
        }
        public async Task<List<string>> GetDistinctVendorsAsync()
        {
            return await _context.Mobile.Select(p => p.Vendor).Distinct().ToListAsync();
        }

        public async Task<List<PhoneCardDto>> GetFilteredPhonesAsync(List<string> vendors, List<string> brands, decimal? minPrice, decimal? maxPrice, string sortBy)
        {
            // Base query
            IQueryable<Phone> query = _context.Mobile;

            // Apply filter for vendors
            if (vendors != null && vendors.Any())
            {
                query = query.Where(p => vendors.Contains(p.Vendor));
            }

            // Apply filter for brands
            if (brands != null && brands.Any())
            {
                query = query.Where(p => brands.Contains(p.Brand));
            }

            // Apply price range filter
            if (minPrice.HasValue)
            {
                query = query.Where(p => p.Price >= minPrice.Value);
            }
            if (maxPrice.HasValue)
            {
                query = query.Where(p => p.Price <= maxPrice.Value);
            }

            // Group by brand and model
            var groupedPhones = query
                .GroupBy(p => new { p.Brand, p.Model }) // Group by both Brand and Model
                .Select(g => new PhoneCardDto
                {
                    Brand = g.Key.Brand,
                    Model = g.Key.Model,
                    WholeNames = g.Select(p => p.WholeName).Distinct().ToList(), // List of all variations
                    CheapestPrice = g.Min(p => p.Price),
                    OfferCount = g.Count()
                });

            // Sorting logic
            switch (sortBy)
            {
                case "price_asc":
                    groupedPhones = groupedPhones.OrderBy(p => p.CheapestPrice);
                    break;
                case "price_desc":
                    groupedPhones = groupedPhones.OrderByDescending(p => p.CheapestPrice);
                    break;
                case "offers_desc":
                    groupedPhones = groupedPhones.OrderByDescending(p => p.OfferCount);
                    break;
                default:
                    groupedPhones = groupedPhones.OrderBy(p => p.Model); // Default sorting
                    break;
            }

            return await groupedPhones.ToListAsync();
        }
        public async Task<List<Phone>> GetOffersForPhoneAsync(string brand, string model)
        {
            // Query the database for all offers matching the provided brand and model
            var offers = await _context.Mobile
                .Where(p => p.Brand == brand && p.Model == model)
                .OrderBy(p=>p.Price)
                .ToListAsync();

            return offers;
        }
    }
}
