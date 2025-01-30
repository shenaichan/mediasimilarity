import { useState } from "react";
import "./App.css";

function App() {
  // const [count, setCount] = useState(0);
  const [mediaList, setMediaList] = useState<string[]>([]);
  const [currInput, setCurrInput] = useState("");

  function submit() {
    setMediaList((mediaList) => [...mediaList, currInput]);
    setCurrInput("");
  }

  return (
    <div id="maincontent">
      <h1>Welcome to SharedTropes!</h1>
      <p>Input yr fav media below to see what tropes they share:</p>
      <input
        value={currInput}
        onChange={(e) => setCurrInput(e.target.value)}
      ></input>
      <button onClick={submit}>submit</button>
      <ul>
        {mediaList.map((elt) => (
          <li key={elt}>{elt}</li>
        ))}
      </ul>
      {/* <button onClick={() => setCount((count) => count + 5)}>
        count is {count}
      </button> */}
    </div>
  );
}

export default App;
