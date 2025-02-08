import { useEffect, useState } from "react";
import "./App.css";

function App() {
  // const [count, setCount] = useState(0);
  const [mediaList, setMediaList] = useState<string[]>([]);
  const [currInput, setCurrInput] = useState("Search for media...");
  const [inputClicked, setInputClicked] = useState(false);
  const [timeoutId, setTimeoutId] = useState(-1);

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

  async function search(query: string): Promise<any> {
    const url = `/api/search?q=${query}`;
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const json = await response.json();
      console.log(json);
    } catch(e) {
      console.error((e as Error).message);
    }
  }

  useEffect(() => {
    clearTimeout(timeoutId);
    const tid = setTimeout(() => {
      console.log("finally stopped typing");
      search(currInput);
    }, 1000);
    setTimeoutId(tid);
  }, [currInput]);


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
