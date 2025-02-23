import React, { useState, useEffect, useRef, useCallback } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import Phones from "../Phones/phonesList";
import Header from "../Header/header";
import Aside from "../Aside/aside";
import PhonesService from "../../repository/phones";
import PhoneDetailsPage from "../PhoneDetailsPage/PhoneDetailsPage";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

const App = () => {
    const navigate = useNavigate();
    const [phones, setPhones] = useState([]);
    const [phoneLength, setPhoneLength] = useState(0);
    const [page, setPage] = useState(0);
    const [filters, setFilters] = useState({
        vendors: [],
        brands: [],
        minPrice: null,
        maxPrice: null,
        sortBy: "price_desc",
    });

    const debounceTimeout = useRef(null);
    const lastFilters = useRef(filters);

    
    const fetchFilteredPhones = useCallback(() => {
        const { vendors, brands, minPrice, maxPrice, sortBy } = filters;

        
        if (JSON.stringify(lastFilters.current) !== JSON.stringify(filters)) {
            PhonesService.fetchFilteredPhones(vendors, brands, minPrice, maxPrice, sortBy)
                .then((response) => {
                    setPhones(response.data);
                    setPhoneLength(response.data.length);
                    lastFilters.current = filters; 
                })
                .catch((error) => console.error("Error fetching filtered phones:", error));
        }
    }, [filters]);

    
    useEffect(() => {
        if (debounceTimeout.current) {
            clearTimeout(debounceTimeout.current);
        }

        debounceTimeout.current = setTimeout(() => {
            fetchFilteredPhones();
        }, 500); 

        return () => clearTimeout(debounceTimeout.current); 
    }, [filters, fetchFilteredPhones]);

    
    const handleFilterChange = (updatedFilters) => {
        navigate("/"); 
        setPage(0); 
        setFilters((prevFilters) => ({
            ...prevFilters,
            ...updatedFilters,
        }));
    };

    return (
        <div style={{ width: '100%', overflow: 'hidden' }}>
            <Header onFilterChange={handleFilterChange} totalOffers={phoneLength} />
            <div className="container-fluid">
                <Routes>
                    <Route
                        path="/"
                        element={
                            <div
                                className="row h-screen w-full bg-cover"
                                style={{
                                    background: "#024950",
                                    background: "linear-gradient(90deg, #024950 0%, #0fa4af 50%, #024950 100%)"
                                }}
                            >
                                <div className="col-md-3">
                                    <Aside onFilterChange={handleFilterChange} />
                                </div>
                                <div className="col-md-9">
                                    <Phones 
                                        allPhones={phones} 
                                        onFilterChange={handleFilterChange} 
                                        page={page} 
                                        setPage={setPage} 
                                    />
                                </div>
                            </div>
                        }
                    />
                    <Route path="/phone-details" element={<PhoneDetailsPage />} />
                </Routes>
            </div>
        </div>
    );
};

export default App;
