using Phonify.Models;
using Phonify.Models.Dto;
using Phonify.Repository;

namespace Phonify.Service
{
    public class PhoneService : IPhoneService
    {
        private readonly IPhoneRepository _repository;
        public PhoneService(IPhoneRepository repository)
        {
            this._repository = repository;
        }
        public async Task<Phone> GetPhoneAsync(int id)
        {
            return await _repository.GetPhoneAsync(id);
        }
        public async Task<List<PhoneCardDto>> GetFilteredPhonesAsync(List<string> vendors, List<string> brands, decimal? minPrice, decimal? maxPrice, string sortBy)
        {
            return await _repository.GetFilteredPhonesAsync(vendors,brands,minPrice,maxPrice,sortBy);
        }

        public async Task<List<Phone>> GetPhoneListAsync()
        {
            return await _repository.GetAllPhonesAsync();
        }
        public async Task<List<Phone>> GetOffersForPhoneAsync(string brand, string model)
        {
            return await _repository.GetOffersForPhoneAsync(brand, model);
        }
        public Task<List<string>> GetDistinctBrandsAsync()
        {
            return _repository.GetDistinctBrandsAsync();
        }

        public Task<List<string>> GetDistinctVendorsAsync()
        {
            return _repository.GetDistinctVendorsAsync();
        }
    }
}
