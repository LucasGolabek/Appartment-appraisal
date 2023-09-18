import React, { useState } from "react";
import "./Search.scss";

const Search = ({ setContent }) => {
  const [area, setArea] = useState("");
  const [room, setRoom] = useState("");
  const [heating, setHeating] = useState("");
  const [location, setLocation] = useState("");

  const handleSubmit = (event) => {
    const userToken = sessionStorage.getItem("token");

    const url = "http://20.234.64.208:8000/apartment/";
    const data = {
      location: location,
      measurement: area,
      rooms: room,
      heating: heating,
    };

    //    const authorization = "Token " + "31e845a3adc224da9293b3ff9c3f20f98268b4e9";

    event.preventDefault();
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + userToken,
      },
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
      .then((response) => {
        if (response.ok) {
          response.json().then((json) => {
            if (json.data){
              setContent(json.data)
            } else {
              alert("Brak wyników dla zadanych parametrów")
            }
          });
        } else {
          alert("Brak wyników dla zadanych parametrów")
        }
      })
  };

  return (
    <>
      <form className="searchContainer" onSubmit={handleSubmit}>
        <div className="defaultContainer searchHeader">
          Ustaw parametry wyszukiwania
        </div>
        <div className="searchInputContainer">
          <label className="defaultContainer searchInputLabel">
            Powierzchnia
          </label>
          <input
            type="text"
            value={area}
            className="defaultContainer searchInputInput"
            placeholder={"Liczba metrów"}
            onChange={(e) => setArea(e.target.value)}
          />
        </div>
        <div className="searchInputContainer">
          <label className="defaultContainer searchInputLabel">
            Liczba pokoi
          </label>
          <input
            type="text"
            value={room}
            className="defaultContainer searchInputInput"
            placeholder={"Liczba pokoi"}
            onChange={(e) => setRoom(e.target.value)}
          />
        </div>
        <div className="searchInputContainer">
          <label className="defaultContainer searchInputLabel">
            Ogrzewanie
          </label>
          <input
            type="text"
            value={heating}
            className="defaultContainer searchInputInput"
            placeholder={"Typ ogrzewania"}
            onChange={(e) => setHeating(e.target.value)}
          />
        </div>
        <div className="searchInputContainer">
          <input
            value={location}
            className="defaultContainer searchInputLabel searchInputInputDouble"
            placeholder={"Ustaw lokalizacje"}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>
        <label className="defaultContainer searchButtonContainer">
          Szukaj
          <input style={{ display: "none" }} type="submit" />
        </label>
      </form>
    </>
  );
};

export default Search;
