import React, { useState, useEffect } from "react";
import PriceSlider from "./priceSlider";
import BrandList from "./brandList";
import VendorList from "./vendorList";
import SortBy from "./sortBy"; // Import the SortBy component
import PhonesService from "../../repository/phones";
import SearchBar from "./searchBar";

const Aside = ({ onFilterChange }) => {
  const [brands, setBrands] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [selectedBrands, setSelectedBrands] = useState([]);
  const [selectedVendors, setSelectedVendors] = useState([]);
  const [priceRange, setPriceRange] = useState([0, 200000]);
  const [sortBy, setSortBy] = useState("price_desc");

  useEffect(() => {
    const fetchBrands = async () => {
      try {
        const response = await PhonesService.fetchBrands();
        setBrands(response.data);
      } catch (error) {
        console.error("Error fetching brands:", error);
      }
    };

    const fetchVendors = async () => {
      try {
        const response = await PhonesService.fetchVendors();
        setVendors(response.data);
      } catch (error) {
        console.error("Error fetching vendors:", error);
      }
    };

    fetchBrands();
    fetchVendors();
  }, []);

  useEffect(() => {
    onFilterChange({
      brands: selectedBrands,
      vendors: selectedVendors,
      minPrice: priceRange[0],
      maxPrice: priceRange[1],
      sortBy: sortBy,
    });
  }, [selectedBrands, selectedVendors, priceRange, sortBy]);
  

  const asideStyles = {
    borderRadius: "0.625rem", 
    padding: "1.25rem", 
    marginTop: "2vh", 
    transition: "all 0.3s ease-in-out",
  };

  const contentStyles = {
    borderRadius: "0.625rem", 
    padding: "15px", 
    boxShadow: "0 0.125rem 0.375rem rgb(255, 255, 255)", 
  };

  
  const responsiveStyles = `
    @media (max-width: 1024px) {
      .aside-container {
        width: 100%;
        margin-top: 1.5vh;
      }
    }

    @media (max-width: 768px) {
      .aside-container {
        position: relative;
        width: 100%;
        margin: 0 auto;
        padding: 1rem;
      }
      .aside-content {
        padding: 1rem;
      }
    }

    @media (max-width: 480px) {
      .aside-container {
        width: 100%;
        padding: 0.75rem;
        margin-top: 1vh;
      }
      .aside-content {
        padding: 0.75rem;
        box-shadow: none;
      }
    }
  `;

  return (
    <>
      <style>{responsiveStyles}</style>
      <aside className="aside-container" style={asideStyles}>
        <div className="aside-content" style={contentStyles}>
          <PriceSlider
            minPrice={priceRange[0]}
            maxPrice={priceRange[1]}
            onPriceChange={(newRange) => setPriceRange(newRange)}
          />
          <BrandList
            brands={brands}
            selectedBrands={selectedBrands}
            onBrandChange={setSelectedBrands}
          />
          <VendorList
            vendors={vendors}
            selectedVendors={selectedVendors}
            onVendorChange={setSelectedVendors}
          />
          <SortBy
            selectedSort={sortBy}
            onSortChange={(newSort) => setSortBy(newSort)}
          />
        </div>
      </aside>
    </>
  );
};

export default Aside;
