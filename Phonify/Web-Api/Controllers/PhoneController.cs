using Microsoft.AspNetCore.Mvc;
using Phonify.Service;
using Phonify.Models;
using Phonify.Models.Dto;
namespace Phonify.Controllers
{
    [Route("/[controller]")]
    [ApiController]
    public class PhoneController : Controller
    {
        private readonly IPhoneService _phoneService;
        public PhoneController(IPhoneService phoneService) { 
            this._phoneService = phoneService;
        }
        [HttpGet("/phones")]
        public async Task<ActionResult<Phone>> getAllPhones()
        {
            var phone = await _phoneService.GetPhoneListAsync();
            return Ok(phone);
        }
        [HttpGet("/phones/{id}")]
        public async Task<ActionResult<Phone>> GetById(int id)
        {
            var phone = await _phoneService.GetPhoneAsync(id);
            return Ok(phone);
        }
        [HttpGet("/phones/getFilteredPhones")]
        public async Task<ActionResult<List<PhoneCardDto>>> GetFilteredPhones([FromQuery] List<string> vendors,
            [FromQuery] List<string> brands,
            [FromQuery] decimal? minPrice,
            [FromQuery] decimal? maxPrice,
            [FromQuery] string? sortBy)
        {
            var phones = await _phoneService.GetFilteredPhonesAsync(vendors,brands,minPrice,maxPrice,sortBy);
            return Ok(phones);
        }
        [HttpGet("/phones/getOffersForPhone")]
        public async Task<ActionResult<List<Phone>>> GetOffersForPhoneAsync([FromQuery] string brand, string model)
        {
            var phones = await _phoneService.GetOffersForPhoneAsync(brand,model);
            return Ok(phones);
        }
        [HttpGet("/phones/brands")]
        public async Task<ActionResult<List<string>>> GetBrands()
        {
            var brands = await _phoneService.GetDistinctBrandsAsync();
            return Ok(brands);
        }
        [HttpGet("/phones/vendros")]
        public async Task<ActionResult<List<string>>> GetVendors()
        {
            var vendors = await _phoneService.GetDistinctVendorsAsync();
            return Ok(vendors);
        }
    }
}
