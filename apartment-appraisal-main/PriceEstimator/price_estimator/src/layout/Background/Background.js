import React from "react";
import BackgroundImage from "../../assets/backgrounds/homePageBackground.jpg";
import "./Background.scss";

const Background = () => {
  return (
    <div className="backgroundContainer">
      <img
        src={BackgroundImage}
        alt="BackgroundImage"
        className="backgroundImage"
      />
    </div>
  );
};

export default Background;
