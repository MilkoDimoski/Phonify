import React, { useState } from "react";
import Slider from "@mui/material/Slider";

const PriceSlider = ({ minPrice, maxPrice, onPriceChange }) => {
  const [sliderValue, setSliderValue] = useState([minPrice, maxPrice]);

  // Handle UI updates during slider interaction
  const handleChange = (event, newValue) => {
    setSliderValue(newValue);
  };

  // Handle final value update after interaction ends
  const handleChangeCommitted = (event, newValue) => {
    onPriceChange(newValue);
  };

  // Inline styles for the container
  const containerStyles = {
    padding: "1rem",
    border: "0.1rem solid #ddd",
    borderRadius: "0.5rem",
    marginTop: "1rem",
    backgroundColor: "#f9f9f9",
    boxShadow: "0 0.5rem 1rem rgba(0, 0, 0, 0.1)",
    transition: "all 0.3s ease-in-out",
  };

  // Responsive styles inside a `<style>` tag
  const responsiveStyles = `
    @media (max-width: 1024px) {
      .price-container {
        width: 100%;
      }
    }

    @media (max-width: 768px) {
      .price-container {
        padding: 0.75rem;
        margin-top: 0.5rem;
      }
      .price-title {
        font-size: 1rem;
      }
    }

    @media (max-width: 480px) {
      .price-container {
        padding: 0.5rem;
        margin-top: 0.5rem;
        box-shadow: none;
      }
    }
  `;

  return (
    <>
      <style>{responsiveStyles}</style>
      <div className="price-container" style={containerStyles}>
        <h5 className="price-title" style={{ fontSize: "1.125rem", color: "#333", marginBottom: "1rem", fontWeight: "600" }}>
          Цена: {sliderValue[0]} – {sliderValue[1]} MKD
        </h5>

        <Slider
          value={sliderValue}
          min={0}
          max={200000}
          onChange={handleChange}
          onChangeCommitted={handleChangeCommitted}
          valueLabelDisplay="auto"
          valueLabelFormat={(value) => `${value} MKD`}
          sx={{
            height: "0.5rem",
            borderRadius: "2rem",
            "& .MuiSlider-thumb": {
              backgroundColor: "#7fcfa8",
              borderRadius: "50%",
              width: "1.5rem",
              height: "1.5rem",
              boxShadow: "0 0.5rem 1rem rgba(0, 0, 0, 0.2)",
              "&:hover": {
                backgroundColor: "#558b71",
              },
            },
            "& .MuiSlider-rail": {
              backgroundColor: "#e0e0e0",
              opacity: 1,
            },
            "& .MuiSlider-track": {
              background: `linear-gradient(to right, #98fbcb ${((sliderValue[0] / 200000) * 100).toFixed(2)}%, rgb(191, 255, 237) ${((sliderValue[1] / 200000) * 100).toFixed(2)}%)`,
              height: "0.5rem",
              borderRadius: "2rem",
            },
          }}
        />
      </div>
    </>
  );
};

export default PriceSlider;
