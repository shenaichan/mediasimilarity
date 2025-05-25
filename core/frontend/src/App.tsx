import { useEffect, useState } from "react";
import "./App.css";

import mediaCategories from "./MediaCategories";

type Media = {
  urlSafeTitle: string;
  urlMediaType: string;
  displayTitle: string;
};

type Trope = {
  urlSafeName: string;
  displayName: string;
};

type SearchState = "empty" | "searching" | "deciding" | "decided";

const constructMediaUrl = (media: Media) => {
  return `https://tvtropes.org/pmwiki/pmwiki.php/${media.urlMediaType}/${media.urlSafeTitle}`;
};

const constructTropeUrl = (trope: Trope) => {
  return `https://tvtropes.org/pmwiki/pmwiki.php/main/${trope.urlSafeName}`;
};

function Input({
  media,
  setMedia,
}: {
  media: Media | null;
  setMedia: (media: Media | null) => void;
}) {
  const [currInput, setCurrInput] = useState("");
  const [mediaOptions, setMediaOptions] = useState<Media[]>([]);
  const [timeoutId, setTimeoutId] = useState(-1);
  const [searching, setSearching] = useState<SearchState>("empty");

  function maybeAddType(elt: Media) {
    const addMedia =
      mediaOptions.filter((item) => item.displayTitle === elt.displayTitle)
        .length > 1;
    if (addMedia) {
      return `${elt.displayTitle} (${
        mediaCategories.find(([type, _]) => type === elt.urlMediaType)![1]
      })`;
    } else {
      return elt.displayTitle;
    }
  }

  useEffect(() => {
    let ignore = false;

    clearTimeout(timeoutId);

    if (currInput.trim()) {
      setSearching("searching");
      const tid = setTimeout(() => {
        // console.log("finally stopped typing");

        const search = async (query: string) => {
          const url = `/api/search?q=${query}`;
          const response = await fetch(url);
          const json: Media[] = await response.json();
          // console.log(json);
          if (!ignore) {
            setMediaOptions(json);
            setSearching("deciding");
          }
        };

        search(currInput.trim());
      }, 300);
      setTimeoutId(tid);
    } else {
      setSearching("empty");
    }

    return () => {
      ignore = true;
    };
  }, [currInput]);

  const asdf = () => {
    if (searching === "empty" || searching === "decided") {
      return null;
    }

    if (searching === "searching") {
      return (
        <div className="mediaoptions">
          <p>Searching...</p>
        </div>
      );
    }

    if (searching === "deciding") {
      return (
        <div className="mediaoptions">
          {mediaOptions.length ? (
            <ul>
              {mediaOptions.map((elt) => (
                <li
                  key={`${elt.urlMediaType}/${elt.urlSafeTitle}`}
                  onClick={() => {
                    setMedia(elt);
                    setSearching("decided");
                  }}
                >
                  {maybeAddType(elt)}
                </li>
              ))}
            </ul>
          ) : (
            <p>Sorry, there are no results for your search!</p>
          )}
        </div>
      );
    }
  };

  return (
    <div className="inputcontainer">
      {searching === "decided" && (
        <p
          onClick={() => {
            setSearching("empty");
            setCurrInput("");
            setMedia(null);
          }}
          className="clearinput"
        >
          ×
        </p>
      )}
      <input
        className="mediainput"
        placeholder="enter media to compare"
        onChange={(e) => {
          setCurrInput(e.target.value);
        }}
        value={media?.displayTitle || currInput}
        disabled={searching === "decided"}
      />
      {asdf()}
    </div>
  );
}

type CompareState = "precompare" | "comparing" | "compared";

type Results = {
  media1: Media | null;
  media2: Media | null;
  tropes: Trope[];
};

function App() {
  const [media1, setMedia1] = useState<Media | null>(null);
  const [media2, setMedia2] = useState<Media | null>(null);

  const [results, setResults] = useState<Results>({
    media1: null,
    media2: null,
    tropes: [],
  });

  const [loading, setLoading] = useState<CompareState>("precompare");

  const [showAbout, setShowAbout] = useState(false);

  const fetchTropes = async () => {
    if (!media1 || !media2) {
      console.error("what");
      return;
    }
    setLoading("comparing");
    const url = `/api/compare?title1=${media1.urlSafeTitle}&type1=${media1.urlMediaType}&title2=${media2.urlSafeTitle}&type2=${media2.urlMediaType}`;
    const response = await fetch(url);
    const json: Trope[] = await response.json();
    setResults({ media1, media2, tropes: json });
    setLoading("compared");
  };

  return (
    <div id="all">
      <div id="infocontainer">
        <div id="info">
          <div id="titlecontainer">
            <div id="titleflex">
              <h1 id="title">TVennTropes</h1>
              <p
                id="about"
                onClick={() => setShowAbout(!showAbout)}
                className={showAbout ? "bolded" : ""}
              >
                about
              </p>
            </div>
            <hr id="divider" />
          </div>
          {showAbout && (
            <p id="infotext">
              T<em>Venn</em>Tropes is a site for discovering shared tropes
              across media, with data pulled from{" "}
              <a
                href="https://tvtropes.org/"
                target="_blank"
                rel="noopener noreferrer"
              >
                tvtropes.org
              </a>
              . Rarest tropes are listed first.
            </p>
          )}
          <div id="controls">
            <Input media={media1} setMedia={setMedia1} />
            <Input media={media2} setMedia={setMedia2} />
            <button
              id="submit"
              disabled={!(media1 && media2) || loading === "comparing"}
              onClick={() => fetchTropes()}
            >
              {loading === "comparing" ? "loading..." : "get shared tropes"}
            </button>
          </div>
        </div>
      </div>
      {loading === "compared" && results.media1 && results.media2 ? (
        <div id="tropescontainer">
          <p id="tropestitle">
            {results.tropes.length === 0 ? "no" : results.tropes.length} trope
            {results.tropes.length === 1 ? "" : "s"} shared between{" "}
            <a
              href={constructMediaUrl(results.media1)}
              target="_blank"
              rel="noopener noreferrer"
            >
              {results.media1.displayTitle}
            </a>{" "}
            &{" "}
            <a
              href={constructMediaUrl(results.media2)}
              target="_blank"
              rel="noopener noreferrer"
            >
              {results.media2.displayTitle}
            </a>
            {results.tropes.length === 0 ? " :(" : ":"}
          </p>
          <div id="tropes">
            {results.tropes.map((elt) => (
              <p key={`${elt.urlSafeName}`}>
                <a
                  href={constructTropeUrl(elt)}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {elt.displayName}
                </a>
              </p>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default App;
