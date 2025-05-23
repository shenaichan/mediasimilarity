import { useEffect, useState } from "react";
import "./App.css";

type media = {
  urlSafeTitle: string;
  urlMediaType: string;
  displayTitle: string;
};

function App() {
  return (
    <div id="all">
      <div id="infocontainer">
        <div id="info">
          <div id="titlecontainer">
            <h1 id="title">TVennTropes</h1>
            <hr id="divider" />
          </div>
          <div id="controls">
            <input
              className="mediainput"
              placeholder="enter media to compare"
            />
            <button id="submit">get shared tropes</button>
            <input
              className="mediainput"
              placeholder="enter media to compare"
            />
          </div>
        </div>
      </div>
      <div id="tropescontainer">
        <h2 id="tropestitle">shared tropes between x & y:</h2>
        <div id="tropes">
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non
            risus. Suspendisse lectus tortor, dignissim sit amet.
          </p>
          <p>
            Maecenas malesuada. Praesent congue erat at massa. Sed cursus turpis
            vitae tortor. Donec posuere vulputate arcu.
          </p>
          <p>
            Phasellus accumsan cursus velit. Vestibulum ante ipsum primis in
            faucibus orci luctus et ultrices posuere cubilia Curae.
          </p>
          <p>
            In ac felis quis tortor malesuada pretium. Pellentesque auctor neque
            nec urna. Proin sapien ipsum, porta a, auctor quis.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
