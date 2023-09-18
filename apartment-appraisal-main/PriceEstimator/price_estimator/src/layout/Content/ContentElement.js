import React from "react";
import "./ContentElement.scss";
import OtoDomLogo from "../../assets/icons/OtoDomLogo.png";

const ContentElement = ({ content }) => {
  const urlArray = content.split("/");
  const urlAddress = urlArray.at(-1);
  const urlAddressParsedShorten = urlAddress.substring(
    0,
    urlAddress.lastIndexOf("-")
  );
  const urlAddressFinished = urlAddressParsedShorten.replaceAll("-", " ");

  // console.log(urlAddressParsedShorten);

  return (
    <div className="contentElementContainer">
      <img src={OtoDomLogo} alt={"Otodom"} className="contentContainerLogo" />
      <a
        className="contentContainerAddress"
        href={"https://otodom.pl" + content}
      >
        {urlAddressFinished}
      </a>
    </div>
  );
};

export default ContentElement;
