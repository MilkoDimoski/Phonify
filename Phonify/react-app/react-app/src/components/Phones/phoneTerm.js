import React, { useCallback, useMemo } from "react";
import { useNavigate } from "react-router-dom";

const PhoneTerm = React.memo((props) => {
  const navigate = useNavigate();

  const formatModelName = useMemo(() => {
    const name = props.term.model.toLowerCase().replace(/\s+/g, '-');
    if (name.startsWith("iphone-14-pro-max") || name.startsWith("iphone-15-plus")) {
      return `${name}-`;
    }
    if (name.startsWith("iphone-se")) {
      return `${name}-2022`;
    }
    if (name.startsWith("rog-phone-6-batman-edition")) {
      return name.replace('-edition', "");
    }
    if (name.startsWith("zenfone-10")) {
      return name.replace('zenfone-10', "zenfone10");
    }
    if (name.startsWith("xiaomi-14-ultra")){
      return name.replace('xiaomi-14-ultra', '14-ultra-new');
    }
    if (name.startsWith("open")) {
      return name.replace('open', 'open-10');
    }
    if (name.startsWith("galaxy-z-fold-6")){
      return name.replace('galaxy-z-fold-6', 'galaxy-z-fold6');
    }
    if (name.startsWith("galaxy-s25-ultra")){
      return name.replace('galaxy-s25-ultra', 'galaxy-s25-ultra-sm-s938');
    }
    if (name.startsWith("galaxy-s25+")){
      return name.replace('galaxy-s25+', 'galaxy-s25-plus-sm-s936');
    }
    if (name.startsWith("galaxy-s25")){
      return name.replace('galaxy-s25', 'galaxy-s25-sm-s931');
    }
    if (name.startsWith("galaxy-z-fold-5")){
      return name.replace('galaxy-z-fold-5', 'galaxy-z-fold5-5g');
    }
    if (name.startsWith("galaxy-z-flip-3")){
      return name.replace('galaxy-z-flip-3', 'galaxy-z-flip3-5g');
    }
    if (name.startsWith("galaxy-z-flip-5")){
      return name.replace('galaxy-z-flip-5', 'galaxy-z-flip5-5g');
    }
    if (name.startsWith("galaxy-z-fold-4")){
      return name.replace('galaxy-z-fold-4', 'galaxy-z-fold4');
    }
    if (name.startsWith("galaxy-s22+")){
      return name.replace('galaxy-s22+', 'galaxy-s22-plus-5g');
    }
    if (name.startsWith("galaxy-s24+")){
      return name.replace('galaxy-s24+', 'galaxy-s24-plus-5g-sm-s926');
    }
    if (name.startsWith("galaxy-s24-ultra")){
      return name.replace('galaxy-s24-ultra', 'galaxy-s24-ultra-5g-sm-s928-stylus');
    }
    return name;
  }, [props.term.model]);

  const formatBrand = useMemo(() => {
    const brandName = props.term.brand.toLowerCase();
    if (brandName.startsWith("one plus")) {
      return brandName.replace('one plus', 'oneplus');
    }
    return brandName;
  }, [props.term.brand]);

  const imageUrl = useMemo(() => {
    return `https://fdn2.gsmarena.com/vv/bigpic/${formatBrand}-${formatModelName}.jpg`;
  }, [formatBrand, formatModelName]);

  const handleCardClick = useCallback(() => {
    navigate(`/phone-details`, { state: { brand: props.term.brand, model: props.term.model, imageLink: imageUrl } });
  }, [navigate, props.term.brand, props.term.model, imageUrl]);

  const handleMouseOver = useCallback((e) => {
    e.currentTarget.style.transform = "scale(1.05)";
    e.currentTarget.style.boxShadow = "0 18px 36px rgb(186, 209, 237)";
  }, []);

  const handleMouseOut = useCallback((e) => {
    e.currentTarget.style.transform = "scale(1)";
    e.currentTarget.style.boxShadow = "0 12px 24px rgba(0, 0, 0, 0.1)";
  }, []);

  return (
    <div
      className="card"
      onClick={handleCardClick}
      onMouseOver={handleMouseOver}
      onMouseOut={handleMouseOut}
      style={{
        cursor: "pointer",
        backgroundColor: "#fff",
        borderRadius: "12px",
        boxShadow: "0 12px 24px rgba(0, 0, 0, 0.1)",
        overflow: "hidden",
        transition: "transform 0.3s ease, box-shadow 0.3s ease",
        margin: "20px",
        width: "100%",
        maxWidth: "280px",
      }}
    >
      <div className="card-body" style={{ padding: "16px", textAlign: "center" }}>
        <img
          src={imageUrl}
          alt={`${props.term.brand} ${props.term.model}`}
          className="card-img-top"
          style={{
            width: "100%",
            height: "auto",
            borderRadius: "10px",
            objectFit: "contain",
            maxHeight: "220px",
            transition: "transform 0.3s ease",
            loading: "lazy", 
          }}
        />
        <h5
          className="card-title"
          style={{
            fontSize: "16px",
            fontWeight: "600",
            color: "#333",
            marginTop: "12px",
            textTransform: "uppercase",
          }}
        >
          {props.term.brand} {props.term.model}
        </h5>
        <p
          className="card-text"
          style={{
            fontSize: "14px",
            color: "#555",
            marginTop: "8px",
          }}
        >
          Cheapest Price: <strong style={{ color: "#964734", fontSize: "18px", fontWeight: "500" }}>
            {props.term.cheapestPrice} ден.
          </strong>
        </p>
        <p
          className="card-text"
          style={{
            fontSize: "14px",
            color: "#777",
          }}
        >
          Offers: {props.term.offerCount}
        </p>
      </div>
    </div>
  );
});

export default PhoneTerm;
