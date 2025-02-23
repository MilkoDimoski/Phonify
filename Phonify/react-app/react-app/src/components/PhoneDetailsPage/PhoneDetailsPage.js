import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import PhonesService from "../../repository/phones";
import Images from "../../vendorImages/vendorImages";
import 'bootstrap/dist/css/bootstrap.min.css';

const PhoneDetailsPage = () => {
    const location = useLocation();
    const { brand, model, imageLink } = location.state; 
    const [offers, setOffers] = useState([]);

    useEffect(() => {
        console.log(brand);
        console.log(model);
        const fetchOffers = async () => {
            try {
                const response = await PhonesService.fetchPhoneOffers(brand, model);
                setOffers(response.data);
            } catch (error) {
                console.error("Failed to fetch offers", error);
            }
        };

        fetchOffers();
    }, [brand, model]);

    return (
        <div className="container py-5">
            {/* Phone Details */}
            <div className="row mb-5">
                <div className="col-md-6 d-flex align-items-center">
                    <img
                        src={imageLink}
                        alt={`${brand} ${model}`}
                        className="img-fluid rounded shadow-sm"
                        style={{ maxHeight: '400px', objectFit: 'contain' }}
                    />
                    <div className="ms-4">
                        <h1 className="display-4 text-dark mb-3">{brand} {model}</h1>
                        <p className="lead text-muted">Explore the best offers for this phone.</p>
                    </div>
                </div>
            </div>

            {/* Offers List */}
            <div>
                <h2 className="h4 mb-4 text-dark">Available Offers</h2>
                {offers.length > 0 ? (
                    <ul className="list-group">
                        {offers.map((offer, index) => {
                            const backgroundColor = index % 2 === 0 ? "#fff" : "#f7f7f7";
                            return (
                                <li
                                    key={index}
                                    className="list-group-item d-flex align-items-center py-2 px-3"
                                    style={{
                                        backgroundColor: backgroundColor,
                                        borderRadius: "8px", 
                                        marginBottom: "10px", 
                                        boxShadow: "0 1px 2px rgba(0, 0, 0, 0.08)", 
                                        transition: "all 0.3s ease",
                                    }}
                                >
                                    {/* Vendor Image */}
                                    {offer.vendor && (
                                        <div style={{ width: "50px", height: "30px" }} className="me-3">
                                            <img
                                                src={Images.getVendorImage(offer.vendor)}
                                                alt={offer.vendor}
                                                style={{
                                                    width: "100%",
                                                    height: "100%",
                                                    objectFit: "contain",
                                                    transition: "transform 0.3s ease",
                                                }}
                                                onMouseOver={(e) => e.currentTarget.style.transform = "scale(1.1)"}
                                                onMouseOut={(e) => e.currentTarget.style.transform = "scale(1)"}
                                            />
                                        </div>
                                    )}

                                    {/* Offer Details */}
                                    <div className="flex-grow-1">
                                        <div className="d-flex flex-column">
                                            <span className="text-muted" style={{ fontSize: "0.8rem" }}>
                                                {offer.vendor}
                                            </span>
                                            <h5 className="text-dark" style={{ fontSize: "1rem", fontWeight: 600, margin: "3px 0" }}>
                                                {offer.wholeName}
                                                <a
                                                    href={offer.link}
                                                    className="text-decoration-none ms-3"
                                                    style={{
                                                        fontSize: "1rem",
                                                        color: "#558b71",
                                                        fontWeight: "500",
                                                        transition: "color 0.3s ease, transform 0.3s ease",
                                                    }}
                                                    onMouseOver={(e) => {
                                                        e.currentTarget.style.color = "#7fcfa8";
                                                        e.currentTarget.style.transform = "scale(1.05)";
                                                    }}
                                                    onMouseOut={(e) => {
                                                        e.currentTarget.style.color = "#558b71";
                                                        e.currentTarget.style.transform = "scale(1)";
                                                    }}
                                                >
                                                    View Offer
                                                </a>
                                            </h5>
                                        </div>
                                    </div>

                                    {/* Price and View Offer */}
                                    <div className="ms-auto text-end">
                                        <span className="text-primary fw-bold" style={{ fontSize: "1rem", marginLeft: "10px" }}>
                                            {offer.price} ден.
                                        </span>
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
                ) : (
                    <p className="text-muted">No offers available for this phone.</p>
                )}
            </div>
        </div>
    );
};

export default PhoneDetailsPage;
