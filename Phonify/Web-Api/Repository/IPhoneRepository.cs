using Phonify.Models;
using Phonify.Models.Dto;

namespace Phonify.Repository
{
    public interface IPhoneRepository
    {
        public Task<Phone> GetPhoneAsync(int id);
        public Task<List<Phone>> GetAllPhonesAsync();
        public Task<List<string>> GetDistinctBrandsAsync();
        public Task<List<string>> GetDistinctVendorsAsync();
        public Task<List<Phone>> GetOffersForPhoneAsync(string brand, string model);

        public Task<List<PhoneCardDto>> GetFilteredPhonesAsync(
   List<string> vendors,
   List<string> brands,
   decimal? minPrice,
   decimal? maxPrice,
   string sortBy);
    }
}
