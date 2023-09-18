import React from "react";
import UserImage from "../../assets/icons/user.png";
import "./Button.scss";

const Button = ({
  label = "Button",
  color = "#F05365",
  buttonHandler = () => {},
  buttonImage =   UserImage
}) => {
  return (
    <button
      className="buttonContainer"
      style={{ backgroundColor: color }}
      onClick={buttonHandler}
    >
      <div className="buttonImageContainer">
        <img src={buttonImage} alt="ButtonImage" className="buttonImage" />
      </div>
      <div className="buttonImageText">{label}</div>
    </button>
  );
};

export default Button;
