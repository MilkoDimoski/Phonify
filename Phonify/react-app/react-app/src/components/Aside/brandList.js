import React, { useState } from "react";

const BrandList = ({ brands, selectedBrands, onBrandChange }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleBrand = (brand) => {
    if (selectedBrands.includes(brand)) {
      onBrandChange(selectedBrands.filter((b) => b !== brand));
    } else {
      onBrandChange([...selectedBrands, brand]);
    }
  };

  const visibleBrands = isExpanded ? brands : brands.slice(0, 5); 

  
  const containerStyles = {
    padding: "1rem",
    border: "0.1rem solid #ddd", 
    borderRadius: "0.5rem",
    marginTop: "1rem",
    backgroundColor: "#f9f9f9",
    boxShadow: "0 0.25rem 0.5rem rgba(0, 0, 0, 0.1)", 
    transition: "all 0.3s ease-in-out",
  };

  
  const responsiveStyles = `
    @media (max-width: 1024px) {
      .brand-container {
        width: 100%;
      }
    }

    @media (max-width: 768px) {
      .brand-container {
        padding: 0.75rem;
        margin-top: 0.5rem;
      }
      .brand-title {
        font-size: 1rem; 
      }
      .brand-label {
        font-size: 0.9rem;
      }
      .show-more {
        font-size: 0.9rem;
      }
    }

    @media (max-width: 480px) {
      .brand-container {
        padding: 0.5rem;
        margin-top: 0.5rem;
        box-shadow: none;
      }
      .brand-checkbox {
        transform: scale(1); 
      }
    }
  `;

  return (
    <>
      <style>{responsiveStyles}</style>
      <div className="brand-container" style={containerStyles}>
        <h4 className="brand-title" style={{ fontSize: "1.125rem", color: "#1A1A1D", fontWeight: "600", marginBottom: "1rem" }}>
          Brands
        </h4>
        {visibleBrands.map((brand) => (
          <div key={brand} style={{ display: "flex", alignItems: "center", marginBottom: "0.75rem" }}>
            <input
              type="checkbox"
              checked={selectedBrands.includes(brand)}
              onChange={() => toggleBrand(brand)}
              className="brand-checkbox"
              style={{
                marginRight: "0.75rem",
                accentColor: "#558b71",
                transform: "scale(1.1)",
                transition: "transform 0.2s ease",
              }}
            />
            <label
              className="brand-label"
              style={{
                fontSize: "1rem",
                color: "#1A1A1D",
                cursor: "pointer",
                transition: "color 0.3s ease",
              }}
              onMouseOver={(e) => (e.target.style.color = "#558b71")}
              onMouseOut={(e) => (e.target.style.color = "#1A1A1D")}
            >
              {brand}
            </label>
          </div>
        ))}

        {/* Show More button */}
        {brands.length > 5 && (
          <span
            className="show-more"
            onClick={() => setIsExpanded(!isExpanded)}
            style={{
              display: "block",
              marginTop: "0.75rem",
              fontSize: "1rem",
              color: "#558b71",
              cursor: "pointer",
              fontWeight: "500",
              transition: "color 0.3s ease, font-weight 0.3s ease",
            }}
            onMouseOver={(e) => {
              e.target.style.color = "#7fcfa8";
              e.target.style.fontWeight = "600";
            }}
            onMouseOut={(e) => {
              e.target.style.color = "#558b71";
              e.target.style.fontWeight = "500";
            }}
          >
            {isExpanded ? "Show Less" : "Show More..."}
          </span>
        )}
      </div>
    </>
  );
};

export default BrandList;
