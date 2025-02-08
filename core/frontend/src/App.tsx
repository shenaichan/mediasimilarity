import { useState } from "react";
import "./App.css";

function App() {
  // const [count, setCount] = useState(0);
  const [mediaList, setMediaList] = useState<string[]>([]);
  const [currInput, setCurrInput] = useState("Search for media...");
  const [inputClicked, setInputClicked] = useState(false);

  function submitOnEnter(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      submit();
    }
  }

  function submit() {
    setMediaList((mediaList) => [...mediaList, currInput]);
    setCurrInput("");
  }

  function activate() {
    if (!inputClicked){
      setCurrInput("");
      setInputClicked(true);
    }
  }

  return (
    <div id="maincontent">
      <div id="searchstuff">
        <h1>t(venn)tropes</h1>
        <input
          style={inputClicked ? {} : {color: "gray", fontStyle: "italic"}}
          value={currInput}
          onClick={activate}
          onChange={(e) => setCurrInput(e.target.value)}
          onKeyDown={submitOnEnter}
        ></input>
        {/* <button onClick={submit}>
          click to submit or you can just press enter
        </button> */}
        <ul>
          {mediaList.map((elt) => (
            <li key={elt}>{elt}</li>
          ))}
        </ul>
        <button
          style={{margin: "5px 0px", width: "fit-content"}}
        >
          Get shared tropes!
        </button>
      </div>
    </div>
  );
}

export default App;
