import React from "react";

const VendorList = ({ vendors, selectedVendors, onVendorChange }) => {
  const toggleVendor = (vendor) => {
    if (selectedVendors.includes(vendor)) {
      onVendorChange(selectedVendors.filter((v) => v !== vendor));
    } else {
      onVendorChange([...selectedVendors, vendor]);
    }
  };

  return (
    <div
      style={{
        padding: "1rem",
        border: "0.125rem solid #ddd",
        borderRadius: "0.5rem",
        marginTop: "1rem",
        backgroundColor: "#f9f9f9",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
      }}
    >
      <h4
        style={{
          fontSize: "1rem",
          color: "#1A1A1D",
          fontWeight: "600",
          marginBottom: "1rem",
        }}
      >
        Vendors
      </h4>
      {vendors.map((vendor) => (
        <div
          key={vendor}
          style={{
            display: "flex",
            alignItems: "center",
            marginBottom: "0.75rem",
            flexDirection: "row", 
          }}
        >
          <input
            type="checkbox"
            checked={selectedVendors.includes(vendor)}
            onChange={() => toggleVendor(vendor)}
            style={{
              marginRight: "0.75rem",
              accentColor: "#558b71",
              transform: "scale(1.1)",
              transition: "transform 0.2s ease",
            }}
          />
          <label
            style={{
              fontSize: "1rem",
              color: "#1A1A1D",
              cursor: "pointer",
              transition: "color 0.3s ease",
            }}
            onMouseOver={(e) => (e.target.style.color = "#7fcfa8")}
            onMouseOut={(e) => (e.target.style.color = "#1A1A1D")}
          >
            {vendor}
          </label>
        </div>
      ))}
      
      {/* Mobile responsiveness using CSS Media Queries */}
      <style jsx>{`
        @media (max-width: 768px) {
          div {
            padding: 0.5rem; /* Less padding on small screens */
          }

          h4 {
            font-size: 0.9rem; /* Slightly smaller heading */
          }

          label {
            font-size: 0.875rem; /* Smaller font size for labels on mobile */
          }

          input {
            transform: scale(1); /* Standard checkbox size on mobile */
          }
        }
      `}</style>
    </div>
  );
};

export default VendorList;
