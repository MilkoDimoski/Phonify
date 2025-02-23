import React from "react";

const SortBy = ({ selectedSort, onSortChange }) => {
  const options = [
    { value: "price_asc", label: "Најефтино" },
    { value: "price_desc", label: "Најскапо" },
    { value: "newest", label: "Најново" },
  ];

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
      <h5
        style={{
          fontSize: "1rem",
          color: "#1A1A1D",
          fontWeight: "600",
          marginBottom: "1rem",
        }}
      >
        Sort By
      </h5>
      <select
        value={selectedSort}
        onChange={(e) => onSortChange(e.target.value)}
        style={{
          padding: "0.625rem",
          fontSize: "1rem",
          color: "#1A1A1D",
          backgroundColor: "#fff",
          border: "0.0625rem solid #ccc",
          borderRadius: "0.3125rem",
          width: "100%",
          cursor: "pointer",
          transition: "all 0.3s ease",
        }}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SortBy;
