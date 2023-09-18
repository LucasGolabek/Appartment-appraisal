import "./HomePage.scss";
import Background from "../../layout/Background";
import React from "react";
import Header from "../../layout/Header";
import Search from "../../layout/Search";
import ContentElement from "../../layout/Content";
import { useState } from "react";
import ContentElementHeader from "../../layout/Content/ContentElementHeader";

const HomePage = () => {
  const [content, setContent] = useState({
    price: 0,
    median: 0,
    probe: 0,
    examples: [],
  });
  return (
    <>
      <Background />
      <Header />
      <div className="contentLayout">
        <div className="contentContainer">
          <ContentElementHeader content={content} />
          {(content.examples && content.examples.length) ? content.examples.map((content) => {
            return <ContentElement content={content} />;
          }) : alert("Brak wyników dla zadanych parametrów")}
        </div>
        <Search setContent={setContent} />
      </div>
    </>
  );
};

export default HomePage;
