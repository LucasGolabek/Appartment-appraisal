import React, { useState } from "react";
import Logo from "../../assets/icons/logo.png";
import Button from "../../components/button";
import UserImage from "../../assets/icons/user.png";
import Register from "../../assets/icons/register.png";
import Logout from "../../assets/icons/logout.png";
import "./Header.scss";

const Header = () => {
  const [showLogin, setShowLogin] = React.useState(false);
  const [showRegister, setShowRegister] = React.useState(false);
  const [loginValue, setLogin] = useState(sessionStorage.getItem("login") ? sessionStorage.getItem("login") : "Wpisz Login");
  const [passwordValue, setPassword] = useState("Wpisz Hasło");
  const [passwordValue2, setPassword2] = useState("Powtórz Hasło");
  const [loggedIn, setLoggedIn] = useState(!!sessionStorage.getItem("token"));

  const login = (event) => {
    event.preventDefault();
    const url = "http://20.234.64.208:8000/login/";
    const data = {
      username: loginValue,
      password: passwordValue,
    };

    fetch(url, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    }).then((response) => {
      if (response.ok) {
        response.json().then((json) => {
          sessionStorage.setItem("token", json.token);
          sessionStorage.setItem("login", loginValue);
          setLoggedIn(true);
        });
        setShowLogin(false)
      } else {
        alert("Nie udało się zalogować")
      }
    });
  };

  const register = (event) => {
    event.preventDefault();
    const url = "http://20.234.64.208:8000/register/";
    const data = {
      username: loginValue,
      password: passwordValue,
      password2: passwordValue2,
    };

    fetch(url, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    }).then((response) => {
      if (response.ok) {
        login(event)
        setShowRegister(false);
      } else {
        alert("Nie udało się zarejestrować. Hasło jest zbyt proste")
      }
    });
  };

  return (
    <div className="headerContainer">
      {showLogin ? (
        <div className="modalContainerHelper">
          <form onSubmit={login} className="contentContainer modalContainer">
            <div className="defaultContainer searchHeader">Zaloguj</div>
            <div className="searchInputContainer">
              <label className="defaultContainer searchInputLabel">Login</label>
              <input
                type="text"
                value={loginValue}
                className="defaultContainer searchInputInput"
                onChange={(e) => setLogin(e.target.value)}
              />
            </div>
            <div className="searchInputContainer">
              <label className="defaultContainer searchInputLabel">Hasło</label>
              <input
                type="password"
                value={passwordValue}
                className="defaultContainer searchInputInput"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <label className="defaultContainer searchButtonContainer">
              Zaloguj
              <input style={{ display: "none" }} type="submit" />
            </label>
            <button className="defaultContainerClose" onClick={() => setShowLogin(false)}>×</button>
          </form>
        </div>
      ) : null}

      {showRegister ? (
        <div className="modalContainerHelper">
          <form onSubmit={register} className="contentContainer modalContainer">
            <div className="defaultContainer searchHeader">Zarejestruj</div>
            <div className="searchInputContainer">
              <label className="defaultContainer searchInputLabel">Login</label>
              <input
                type="text"
                value={loginValue}
                className="defaultContainer searchInputInput"
                onChange={(e) => setLogin(e.target.value)}
              />
            </div>
            <div className="searchInputContainer">
              <label className="defaultContainer searchInputLabel">Hasło</label>
              <input
                type="password"
                value={passwordValue}
                className="defaultContainer searchInputInput"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="searchInputContainer">
              <label className="defaultContainer searchInputLabel">
                Powtórz hasło
              </label>
              <input
                type="password"
                value={passwordValue2}
                className="defaultContainer searchInputInput"
                onChange={(e) => setPassword2(e.target.value)}
              />
            </div>
            <label className="defaultContainer searchButtonContainer">
              Zarejestruj
              <input style={{ display: "none" }} type="submit" />
            </label>
            <button className="defaultContainerClose" onClick={() => setShowRegister(false)}>×</button>
          </form>
        </div>
      ) : null}

      <div className="headerContainerHelper">
        <img className="headerLogoContainer" src={Logo} alt="Logo" />
        <div className="headerButtonsContainer">
          {loggedIn ? (
            <>
              <Button
                label={loginValue}
                color={"#F05365"}
                buttonImage={UserImage}
                buttonHandler={() => {}}
              />
              <Button
                label={"Wyloguj"}
                color={"#4E5283"}
                buttonImage={Logout}
                buttonHandler={() => {
                  sessionStorage.setItem("token", null);
                  sessionStorage.setItem("login", null);
                  setLoggedIn(false);
                }}
              />
            </>
          ) : (
            <>
              <Button
                label={"Zaloguj"}
                color={"#F05365"}
                buttonImage={UserImage}
                buttonHandler={() => {
                  setShowLogin(true);
                }}
              />
              <Button
                label={"Zarejestruj"}
                color={"#4E5283"}
                buttonImage={Register}
                buttonHandler={() => {
                  setShowRegister(true);
                }}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Header;
