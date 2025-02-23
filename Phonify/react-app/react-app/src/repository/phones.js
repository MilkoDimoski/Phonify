import axios from "../custom-axios/axios";

const PhonesService = {
    fetchBrands: () => {
        return axios.get("/phones/brands");
    },
    fetchVendors: () => {
        return axios.get("/phones/vendros");
    },
    fetchFilteredPhones: (vendors = [], brands = [], minPrice = null, maxPrice = null, sortBy = "popular") => {
        const params = new URLSearchParams();
    
        // Append vendors to the query
        vendors.forEach((vendor) => params.append("vendors", vendor));
    
        // Append brands to the query
        brands.forEach((brand) => params.append("brands", brand));
    
        // Add price range to the query
        if (minPrice !== null) params.append("minPrice", minPrice);
        if (maxPrice !== null) params.append("maxPrice", maxPrice);
    
        // Add sorting option to the query
        if (sortBy) params.append("sortBy", sortBy);
    
        return axios.get(`/phones/getFilteredPhones?${params.toString()}`);
    },
    fetchPhoneOffers: (brand="",model="") => {
        return axios.get(`/phones/getOffersForPhone?brand=${brand}&model=${model}`);
    },
};

export default PhonesService;
