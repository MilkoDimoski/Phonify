import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';

const Header = ({ onFilterChange, totalOffers }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const currentDate = new Date().toLocaleDateString("mk-MK", {
        day: "numeric",
        month: "long",
        year: "numeric",
    });

    

    const brands = ["Xiaomi", "Samsung", "Apple", "Huawei", "Motorola", "OnePlus", "Honor"];
    
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isMobileView, setIsMobileView] = useState(false);

    useEffect(() => {
        const updateView = () => {
            setIsMobileView(window.innerWidth <= 768); 
        };

        window.addEventListener('resize', updateView);
        updateView(); 

        return () => {
            window.removeEventListener('resize', updateView);
        };
    }, []);

    const handleFilterChange = (value) => {
        console.log("Brand selected:", value);
        onFilterChange({ brands: [value] });
        navigate("/");
    };

    const handleLogoClick = () => {
        navigate("/");
    };

    const isDetailsPage = location.pathname === "/phone-details";

    const handlePrev = () => {
        setCurrentIndex((prevIndex) => (prevIndex - 3 + brands.length) % brands.length);
    };

    const handleNext = () => {
        setCurrentIndex((prevIndex) => (prevIndex + 3) % brands.length);
    };

    return (
        <header style={{
           // backgroundColor: "rgba(9,32,63,1)"
            backgroundColor: "#003135"
        }}>
            <div
                className="container py-3 px-4"
                style={{
                    //backgroundColor: "rgba(9,32,63,1)",
                    backgroundColor: "#003135",
                    borderRadius: "8px",
                    wordWrap: "break-word", 
                }}
            >
                <div className="row">
                    <div className="col-12 d-flex justify-content-between align-items-center">
                        <span style={{ color: "white" }}>
                            Вкупно: <strong>{totalOffers}</strong> понуди
                        </span>
                        <span style={{ color: "white" }}>
                            Обновено: <strong>{currentDate}</strong>
                        </span>
                    </div>

                    <div className="col-12 text-center mt-2">
                        <h1
                            className="display-4 fw-bold"
                            style={{
                                color: "#212529",
                                cursor: "pointer",
                                fontFamily: "'Roboto', sans-serif",
                                letterSpacing: "1px",
                                transition: "transform 0.3s ease",
                                marginBottom: "15px", 
                                fontSize: isMobileView ? "2rem" : "3rem", 
                                color: "white"
                            }}
                            onClick={handleLogoClick}
                            onMouseOver={(e) => e.target.style.transform = "scale(1.05)"}
                            onMouseOut={(e) => e.target.style.transform = "scale(1)"}
                        >
                            Phonify
                        </h1>
                    </div>

                    {!isDetailsPage && (
                        <div className="col-12 text-center">
                            {/* Check if the screen is mobile-sized and brands overflow */}
                            {isMobileView ? (
                                <div className="d-flex justify-content-center align-items-center">
                                    <button
                                        className="btn btn-outline-light mx-2"
                                        onClick={handlePrev}
                                        style={{
                                            backgroundColor: "transparent",
                                            color: "white",
                                            border: '2px solid #f0f0f0',
                                            borderRadius: "50%",
                                            fontWeight: "500",
                                            padding: "8px 16px",
                                            fontSize: "14px",
                                            transition: "transform 0.3s ease, background-color 0.3s ease",
                                            boxShadow: "0 2px 5px rgba(0, 0, 0, 0.05)",
                                        }}
                                    >
                                        &lt;
                                    </button>

                                    {brands.slice(currentIndex, currentIndex + 3).map((brand) => (
                                        <button
                                            key={brand}
                                            className="btn btn-outline-light mx-2"
                                            onClick={() => handleFilterChange(brand)}
                                            style={{
                                                backgroundColor: "transparent",
                                                color: "white",
                                                border: '2px solid #f0f0f0',
                                                borderRadius: "20px",
                                                fontWeight: "500",
                                                padding: "8px 16px",
                                                fontSize: "14px",
                                                transition: "transform 0.3s ease, background-color 0.3s ease",
                                                boxShadow: "0 2px 5px rgba(0, 0, 0, 0.05)",
                                            }}
                                            onMouseOver={(e) => {
                                                e.target.style.backgroundColor = "#f0f0f0";
                                                e.target.style.transform = "scale(1.05)";
                                            }}
                                            onMouseOut={(e) => {
                                                e.target.style.backgroundColor = "transparent";
                                                e.target.style.transform = "scale(1)";
                                            }}
                                        >
                                            {brand}
                                        </button>
                                    ))}

                                    <button
                                        className="btn btn-outline-light mx-2"
                                        onClick={handleNext}
                                        style={{
                                            backgroundColor: "transparent",
                                            color: "white",
                                            border: '2px solid #f0f0f0',
                                            borderRadius: "50%",
                                            fontWeight: "500",
                                            padding: "8px 16px",
                                            fontSize: "14px",
                                            transition: "transform 0.3s ease, background-color 0.3s ease",
                                            boxShadow: "0 2px 5px rgba(0, 0, 0, 0.05)",
                                        }}
                                    >
                                        &gt;
                                    </button>
                                </div>
                            ) : (
                                <div className="d-flex justify-content-center flex-wrap">
                                    {brands.map((brand) => (
                                        <button
                                            key={brand}
                                            className="btn btn-outline-light mx-2"
                                            onClick={() => handleFilterChange(brand)}
                                            style={{
                                                backgroundColor: "transparent",
                                                color: "white",
                                                border: '2px solid #f0f0f0',
                                                borderRadius: "20px",
                                                fontWeight: "500",
                                                padding: "8px 16px",
                                                fontSize: "14px",
                                                transition: "transform 0.3s ease, background-color 0.3s ease",
                                                boxShadow: "0 2px 5px rgba(0, 0, 0, 0.05)",
                                            }}
                                            onMouseOver={(e) => {
                                                e.target.style.backgroundColor = "rgba(255, 255, 255, 0.66)";
                                                e.target.style.transform = "scale(1.05)";
                                            }}
                                            onMouseOut={(e) => {
                                                e.target.style.backgroundColor = "transparent";
                                                e.target.style.transform = "scale(1)";
                                            }}
                                        >
                                            {brand}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
};

export default Header;