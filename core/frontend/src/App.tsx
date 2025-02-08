import { useEffect, useState } from "react";
import "./App.css";

type media = {
  urlSafeTitle: string;
  urlMediaType: string;
  displayTitle: string;
};

function App() {
  // const [count, setCount] = useState(0);
  const [mediaList, setMediaList] = useState<media[]>([]);
  const [currInput, setCurrInput] = useState("Search for media...");
  const [inputActivated, setInputActivated] = useState(false);
  const [timeoutId, setTimeoutId] = useState(-1);

  // function submitOnEnter(e: React.KeyboardEvent<HTMLInputElement>) {
  //   if (e.key === "Enter") {
  //     submit();
  //   }
  // }

  // function submit() {
  //   setMediaList((mediaList) => [...mediaList, currInput]);
  //   setCurrInput("");
  // }

  function activate() {
    if (!inputActivated) {
      setCurrInput("");
      setInputActivated(true);
    }
  }

  async function search(query: string): Promise<any> {
    const url = `/api/search?q=${query}`;
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const json: media[] = await response.json();
      setMediaList(json);
      console.log(json);
    } catch (e) {
      console.error((e as Error).message);
    }
  }

  useEffect(() => {
    clearTimeout(timeoutId);
    if (inputActivated && currInput.trim()) {
      const tid = setTimeout(() => {
        console.log("finally stopped typing");
        search(currInput);
      }, 1000);
      setTimeoutId(tid);
    }
  }, [currInput]);

  function maybeAddType(elt: media) {
    const addMedia =
      mediaList.filter((item) => item.displayTitle === elt.displayTitle)
        .length > 1;
    if (addMedia) {
      return `${elt.displayTitle} (${elt.urlMediaType})`;
    } else {
      return elt.displayTitle;
    }
  }

  return (
    <div id="maincontent">
      <div id="searchstuff">
        <h1>t(venn)tropes</h1>
        <input
          style={inputActivated ? {} : { color: "gray", fontStyle: "italic" }}
          value={currInput}
          onClick={activate}
          onChange={(e) => setCurrInput(e.target.value)}
          // onKeyDown={submitOnEnter}
        ></input>
        {/* <button onClick={submit}>
          click to submit or you can just press enter
        </button> */}
        <ul>
          {mediaList.map((elt) => (
            <li key={`${elt.urlMediaType}/${elt.urlSafeTitle}`}>
              <a
                href={`https://tvtropes.org/pmwiki/pmwiki.php/${elt.urlMediaType}/${elt.urlSafeTitle}`}
              >
                {maybeAddType(elt)}
              </a>
            </li>
          ))}
        </ul>
        <button style={{ margin: "5px 0px", width: "fit-content" }}>
          Get shared tropes!
        </button>
      </div>
    </div>
  );
}

export default App;
