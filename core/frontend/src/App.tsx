import { useEffect, useState } from "react";
import "./App.css";

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
      return `${elt.displayTitle} (${elt.urlMediaType})`;
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
        console.log("finally stopped typing");

        const search = async (query: string) => {
          const url = `/api/search?q=${query}`;
          const response = await fetch(url);
          const json: Media[] = await response.json();
          console.log(json);
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
    <>
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
    </>
  );
}

function App() {
  const [media1, setMedia1] = useState<Media | null>(null);
  const [media2, setMedia2] = useState<Media | null>(null);

  const [tropes, setTropes] = useState<Trope[]>([]);

  const [loading, setLoading] = useState(false);

  const fetchTropes = async () => {
    if (!media1 || !media2) {
      console.error("what");
      return;
    }
    setLoading(true);
    const url = `/api/compare?title1=${media1.urlSafeTitle}&type1=${media1.urlMediaType}&title2=${media2.urlSafeTitle}&type2=${media2.urlMediaType}`;
    const response = await fetch(url);
    const json: Trope[] = await response.json();
    setTropes(json);
    setLoading(false);
  };

  return (
    <div id="all">
      <div id="infocontainer">
        <div id="info">
          <div id="titlecontainer">
            <h1 id="title">TVennTropes</h1>
            <hr id="divider" />
          </div>
          <div id="controls">
            <Input media={media1} setMedia={setMedia1} />
            <button
              id="submit"
              disabled={!(media1 && media2) || loading || tropes.length > 0}
              onClick={() => fetchTropes()}
            >
              {loading ? "loading..." : "get shared tropes"}
            </button>
            <Input media={media2} setMedia={setMedia2} />
          </div>
        </div>
      </div>
      {tropes.length && media1 && media2 ? (
        <div id="tropescontainer">
          <p id="tropestitle">
            tropes shared between{" "}
            <a
              href={constructMediaUrl(media1)}
              target="_blank"
              rel="noopener noreferrer"
            >
              {media1.displayTitle}
            </a>{" "}
            &{" "}
            <a
              href={constructMediaUrl(media2)}
              target="_blank"
              rel="noopener noreferrer"
            >
              {media2.displayTitle}
            </a>
            :
          </p>
          <div id="tropes">
            {tropes.map((elt) => (
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
