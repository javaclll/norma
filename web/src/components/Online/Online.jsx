import { DndProvider } from "react-dnd";
import { useContext, useState, useEffect } from "react";
import { HTML5Backend } from "react-dnd-html5-backend";
import board from "../../statics/board.svg";
import CoRe from "../Common/ConditionalRendering";
import Goat from "../Goat/Goat.jsx";
import Intersection from "../Intersection/Intersection.jsx";
import Tiger from "../Tiger/Tiger.jsx";
import { GameContext } from "../../context/GameContext";
import configs, { ItemTypes } from "../../utils/config";
import { cloneDeep, create } from "lodash";
import { Link } from "react-router-dom";
import arrow from "../../statics/arrow.svg";
import "../Board/styles/board.css";
import "./styles/online.css";
import tiger from "../../statics/tiger.svg";
import goat from "../../statics/goat.svg";
import replay from "../../statics/replay.svg";
import callAPI from "../../utils/API";

const Online = () => {
  const onClickHandler = () => {
    window.location = "/";
  };

  const [notifShow, setNotif] = useState(false);
  const [player, setPlayer] = useState(0);
  const [link, setLink] = useState(false);
  const [gameID, setGameID] = useState("");

  const sessionResponseFormatter = (value) => {
    if (!value.data) {
      return null;
    }
    let _session = {
      success: value.data.success,
      ident: value.data.ident,
    };
    return _session;
  };

  const gameFormatter = (value) => {
    if (!value.data) {
      return null;
    }
    let gameF = {
      success: value.data.success,
      piece: value.data.piece,
      game_id: value.data.game_id,
    };
    return gameF;
  };

  useEffect(async () => {
    const req = await callAPI({
      endpoint: `/ident`,
      method: "POST",
    });
    const sess = sessionResponseFormatter(req);
    const currentSess = localStorage.getItem("ident");
    console.log(currentSess);
    if (sess && sess.success && !currentSess) {
      localStorage.setItem("ident", sess.ident);
    }
    console.log(sess);
  }, []);

  const createGame = async (player) => {
    setPlayer(player);
    const req = await callAPI({
      endpoint: `/create-game`,
      method: "POST",
      params: { preference: player, ident: localStorage.getItem("ident"), with_norma: true },
    });
    const gameD = gameFormatter(req);
    if (gameD && gameD.success) {
      setGameID(gameD.game_id);
    }
  };
  return (
    <>
      <CoRe condition={player == 0}>
        <div className="player_overlay">
          <div className="player_title">Select your Player</div>
          <div className="player_select">
            <div
              className="player"
              onClick={() => {
                createGame(-1);
              }}
            >
              <img src={tiger} className="select_image" />
            </div>
            <div
              className="player"
              onClick={() => {
                createGame(1);
              }}
            >
              <img src={goat} className="select_image" />
            </div>
          </div>
        </div>
      </CoRe>
      <CoRe condition={player != 0 && !link}>
        <div className="share_overlay">
          <div className="share_container">
            <div className="share_title">
              Share this link with anyone to play
            </div>
            <div className="share_box">
              <input
                type="text"
                className="share_link"
                value={configs.C_HOST + `/play?game_id=${gameID}`}
              />
              <button
                className="copyButton"
                type="button"
                onClick={(e) => {
                  navigator.clipboard.writeText(
                    configs.C_HOST + `/play?game_id=${gameID}`
                  );
                  setNotif(true);
                  setTimeout(function () {
                    setNotif(false);
                  }, 1500);
                }}
              >
                <a className="copy_text">Copy</a>
              </button>
            </div>
            <div className="share_GoTo">
              <button
                className="startButton button_color4"
                type="button"
                onClick={(e) => {
                  window.location = `/play?game_id=${gameID}`;
                }}
              >
                <a className="menu_text">Start Game</a>
              </button>
            </div>
            <div className="share_copy">
              {notifShow ? <a className="c_Notif">Copied to Clipboard</a> : ""}
            </div>
          </div>
        </div>
      </CoRe>
    </>
  );
};
export default Online;
