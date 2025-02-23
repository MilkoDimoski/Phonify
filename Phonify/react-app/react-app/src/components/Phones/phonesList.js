import React, { useState, useMemo, useEffect, useCallback } from "react";
import PhoneTerm from "../Phones/phoneTerm";
import ReactPaginate from "react-paginate";
import SearchBar from "../Aside/searchBar";

const Phones = ({ allPhones, onFilterChange, page, setPage }) => {
  const [size, setSize] = useState(9);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(false);

  const onSearchBarChange = useCallback((text) => {
    setLoading(true);
    setSearchTerm(text);
    setPage(0);
  
    setTimeout(() => {
      setLoading(false);
    }, 300); // Debounce for 300ms
  }, [setPage]);

  const filteredPhones = useMemo(() => {
    return allPhones.filter((phone) => {
      const fullName = `${phone.brand} ${phone.model}`.toLowerCase();
      return fullName.includes(searchTerm.toLowerCase());
    });
  }, [allPhones, searchTerm]);

  const pageCount = Math.ceil(filteredPhones.length / size);

  const currentPhones = useMemo(() => {
    const offset = page * size;
    return filteredPhones.slice(offset, offset + size);
  }, [filteredPhones, page, size]);

  const handlePageClick = (data) => {
    setPage(data.selected);
    window.scrollTo(0, 0);
  };

  const handleSizeChange = (e) => {
    setSize(parseInt(e.target.value, 10));
    setPage(0); 
  };

  useEffect(() => {
    if (searchTerm) {
      setLoading(true);
      const timer = setTimeout(() => setLoading(false), 500);
      return () => clearTimeout(timer);
    }
  }, [searchTerm, currentPhones]);

  return (
    <div className="container mt-5">
      <SearchBar onSearchBarChange={onSearchBarChange} />

      <div className="mb-3" style={{ marginLeft: "60px" }}>
        <label htmlFor="pageSizeSelect" className="form-label" style={{ fontSize: "16px", color: "white" }}>
          Items per page:
        </label>
        <select
          id="pageSizeSelect"
          className="form-select w-auto ms-2"
          value={size}
          onChange={handleSizeChange}
          style={{
            backgroundColor: "#fff",
            borderColor: "#558b71",
            color: "#1A1A1D",
            fontSize: "16px",
            transition: "border-color 0.3s ease",
          }}
        >
          <option value={9}>9</option>
          <option value={21}>21</option>
          <option value={30}>30</option>
        </select>
      </div>

      
        <div
          className="row justify-content-center"
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "20px",
            margin: "0 auto",
          }}
        >
          {currentPhones.map((term, index) => (
            <PhoneTerm key={index} term={term} />
          ))}
        </div>


      <ReactPaginate
        previousLabel={"back"}
        nextLabel={"next"}
        breakLabel={"..."}
        pageCount={pageCount}
        forcePage={page} 
        onPageChange={handlePageClick}
        containerClassName={"pagination justify-content-center mt-4"}
        activeClassName={"active"}
      />
      <style>
        {`
          .pagination {
            display: flex;
            gap: 10px;
            color: white;
          }

          .pagination li {
            list-style: none;
          }

          .pagination .active a {
            background-color:rgb(157, 84, 65);
            color: white;
            border-radius: 4px;
            padding: 5px 10px;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(25, 64, 45, 0.4);
            transform: scale(1.1);
            transition: background-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
          }

          .pagination a {
            text-decoration: none;
            color:white;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
          }

          .pagination a:hover {
            background-color:#964734;
            box-shadow: 0 4px 8px rgba(36, 59, 48, 0.4);
            transform: scale(1.1);
          }

          .pagination .disabled a {
            color: #ccc;
            pointer-events: none;
          }

          @media (max-width: 768px) {
            .row {
              gap: 15px;
            }
          }

          @media (max-width: 480px) {
            .row {
              gap: 10px;
            }
          }
        `}
      </style>
    </div>
  );
};

export default Phones;
