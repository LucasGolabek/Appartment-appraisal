import React from "react";
import "./ContentElement.scss";
import chartImage from "../../assets/images/chart2.png";

const ContentElementHeader = ({ content }) => {
  return (
    <div className="contentElementContainerHeader">
      {content?.price ? (
        <>
          <img
            src={chartImage}
            alt={"Chart"}
            className="contentContainerHeaderLogo"
          />
          <div className="contentElementContainerContent">
            <p>Cena : {content?.price.toFixed(2)}zł</p>

            <p>Mediana cen w okolicy : {content?.median.toFixed(2)}zł</p>
            <p>Wymagania spełniło : {content?.probe} ogłoszeń</p>
          </div>
        </>
      ) : (
        <> Uzupełnij pole wyszukiwania, żeby rozpocząć </>
      )}
    </div>
  );
};

export default ContentElementHeader;
