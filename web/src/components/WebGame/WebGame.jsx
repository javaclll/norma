import { DndProvider } from "react-dnd";
import { useContext, useEffect, useState } from "react";
import { HTML5Backend } from "react-dnd-html5-backend";
import board from "../../statics/board.svg";
import CoRe from "../Common/ConditionalRendering";
import Goat from "../Goat/Goat.jsx";
import WebSockIntersection from "./WebSockIntersection";
import Tiger from "../Tiger/Tiger.jsx";
import { ItemTypes } from "../../utils/config";
import { cloneDeep } from "lodash";
import { Link } from "react-router-dom";
import useSocket from "../../utils/useSocket";
import arrow from "../../statics/arrow.svg";
import "../Board/styles/board.css";
import tiger from "../../statics/tiger.svg";
import goat from "../../statics/goat.svg";
import replay from "../../statics/replay.svg";
import { useLocation } from "react-router-dom";
import { OnlineGameContext } from "../../context/OnlineGameContext";
import { WebsocketContext } from "../../utils/WebSocketContext";
import { OnlineGameProvider } from "../../context/OnlineGameContext";

const WebGame = () => {
  const {
    game,
    gameResult,
    turn,
    setTurn,
    goatsCaptured,
    goatCounter,
    nextMove,
    previousMove,
    moveCounter,
    moveHistory,
    playFromThisPoint,
    placeGoat,
    makeMove,
    pgn,
  } = useContext(OnlineGameContext);

  const onClickHandler = () => {
    window.location = "/";
  };

  const PGNtoCord = ({ source: [x, y], target: [m, n] }) => {
    let secondChar = y === "X" ? y : (5 - parseInt(y)).toString();
    let fourthChar = (5 - parseInt(n)).toString();

    // let fourthChar = m.toString();
    let [firstChar, thirdChar] = [x, m].map((item) => {
      switch (item) {
        case "A":
          return "0";
        case "B":
          return "1";
        case "C":
          return "2";
        case "D":
          return "3";
        case "E":
          return "4";
        default:
          return "X";
      }
    });
    return secondChar + firstChar + fourthChar + thirdChar;
  };

  // useEffect(() => {
  //   console.log(turn + " hello");
  // }, [turn]);

  const onMessage = (event) => {
    let data = JSON.parse(event.data);
    if (playerType === 0 && data.type === 8) {
      setPlayerType(data.piece);
    }
    if (data.type === 5) {
      const temp = data.move.split("");
      const temp2 = PGNtoCord({
        source: [temp[0], temp[1]],
        target: [temp[2], temp[3]],
      });

      const finalcut = temp2.split("");

      if (finalcut[0] == "X") {
        placeGoat({ target: [finalcut[2], finalcut[3]] });
      } else {
        makeMove({
          source: [finalcut[0], finalcut[1]],
          target: [finalcut[2], finalcut[3]],
        });
        // if (eval_move["isValid"]) {
        //   let captured = eval_move["isCaptureMove"];
        //   if (captured) {
        //     new_state[eval_move["capturePiece"][0]][
        //       eval_move["capturePiece"][1]
        //     ] = 0;
        //     goatsCap++;
        //   }
        //   new_state[finalcut[2]][finalcut[3]] =
        //     new_state[finalcut[0]][finalcut[1]];
        //   new_state[finalcut[0]][finalcut[1]] = 0;
        //   // let gameStatusAfterMove = gameStatusCheck(
        //   //   new_state,
        //   //   eval_move["isCaptureMove"]
        //   // );
        //   // if (gameStatusAfterMove.decided === true) {
        //   //   setGameResult(gameStatusAfterMove);
        //   // }
        // }
      }
    }
  };

  const onConnect = (event) => {
    event.currentTarget.send(JSON.stringify({ type: 9 }));
  };

  const [playerType, setPlayerType] = useState(0);

  const [websocket] = useSocket({
    onMessage: onMessage,
    onConnect: onConnect,
    websock_host: `ws://localhost:8080/game?id=${
      window.location.search.split("=")[1]
    }&ident=${localStorage.getItem("ident")}`,
    fire:
      localStorage.getItem("ident") &&
      window.location.search.split("=")[1] != null,
  });

  const sendMessage = ({ type, move }) => {
    websocket.send(JSON.stringify({ type: type, move: move }));
  };

  const [notifShow, setNotif] = useState(false);
  return (
    <WebsocketContext.Provider value={websocket}>
      <DndProvider backend={HTML5Backend}>
        <div className="main-container">
          <div className="left-box">
            <div className="left-box-content">
              <div className="button-panel">
                <button
                  className="backward button"
                  onClick={previousMove}
                  disabled={moveCounter === 0}
                >
                  <img className="arrow" src={arrow} />
                </button>
                <div className="move-number text">{moveCounter}</div>
                <button
                  className="forward button"
                  onClick={nextMove}
                  disabled={moveCounter === moveHistory.length - 1}
                >
                  <img className="arrow" src={arrow} />
                </button>
                <button
                  className="replay-bt button"
                  onClick={playFromThisPoint}
                  disabled={moveCounter === moveHistory.length - 1}
                >
                  <img className="replay" src={replay} />
                </button>
              </div>
              <div className="detail-box">
                <CoRe condition={!gameResult.decided}>
                  <h2>
                    You Chose{" "}
                    {playerType === 1
                      ? "Goat"
                      : playerType === -1
                      ? "Tiger"
                      : ""}
                  </h2>
                  <h2>{turn === ItemTypes.GOAT ? "Goat" : "Tiger"}'s Turn</h2>
                </CoRe>
                <CoRe condition={gameResult.decided}>
                  <h2>{gameResult.wonBy === -1 ? "Tiger" : "Goat"} Won!</h2>
                </CoRe>
                <h2>Captured Goats: {goatsCaptured}</h2>
                <h2>Placed Goats: {goatCounter}</h2>
                <h2>History Length: {moveHistory.length - 1}</h2>
              </div>
            </div>
            {gameResult.decided ? (
              <>
                <div className="win-screen">
                  <div className="win-screen-top">
                    <img
                      src={turn === ItemTypes.GOAT ? tiger : goat}
                      className="win-screen-img"
                    />
                    <a className="win-screen-text">
                      {turn === ItemTypes.GOAT ? "Tiger" : "Goat"} Wins!
                    </a>
                  </div>
                  <div className="win-screen-bottom">
                    <button
                      className="win-screen-play-again-button"
                      onClick={(e) => onClickHandler(e)}
                    >
                      Play again!
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <></>
            )}
          </div>

          <div className="board" style={{ backgroundImage: `url(${board})` }}>
            <div className="tableDiv">
              <table className="boardTable">
                <tbody>
                  {game.map((row, rowIndex) => (
                    <tr className="row" key={rowIndex}>
                      {row.map((value, colIndex) => (
                        <WebSockIntersection
                          x={rowIndex}
                          y={colIndex}
                          key={`(${rowIndex},${colIndex})`}
                        >
                          <CoRe condition={value === 1}>
                            <Goat m={rowIndex} n={colIndex} />
                          </CoRe>
                          <CoRe condition={value === -1}>
                            <Tiger m={rowIndex} n={colIndex} />
                          </CoRe>
                        </WebSockIntersection>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="right-box">
            <div className="right-box-content">
              <div className="right-box-content-top">
                <a className="right-box-title text">Played Moves</a>
              </div>
              <div className="right-box-content-bottom">{pgn.join(" - ")}</div>
              <div className="navButtonBox">
                <Link to="/analysis">
                  <button
                    className="navButton"
                    type="button"
                    onClick={(e) => {}}
                  >
                    <a className="nav_text">Go to Analysis Board</a>
                  </button>
                </Link>
              </div>
              <div className="copyButtonBox">
                {notifShow ? (
                  <a className="c_Notif">Copied to Clipboard</a>
                ) : (
                  ""
                )}
                <button
                  className="copyButton"
                  type="button"
                  onClick={(e) => {
                    navigator.clipboard.writeText(pgn.join("-"));
                    setNotif(true);
                    setTimeout(function () {
                      setNotif(false);
                    }, 1500);
                  }}
                >
                  <a className="copy_text">Copy</a>
                </button>
              </div>
            </div>
          </div>
        </div>
      </DndProvider>

      {gameResult.decided ? (
        <>
          <div className="win-screen">
            <div className="win-screen-top">
              <img
                src={gameResult.wonBy === ItemTypes.GOAT ? goat : tiger}
                className="win-screen-img"
              />
              <a className="win-screen-text">
                {gameResult.wonBy === ItemTypes.GOAT ? "Goat" : "Tiger"} Wins!
              </a>
            </div>
            <div className="win-screen-bottom">
              <button
                className="win-screen-play-again-button"
                onClick={(e) => onClickHandler(e)}
              >
                Play again!
              </button>
            </div>
          </div>
        </>
      ) : (
        <></>
      )}
    </WebsocketContext.Provider>
  );
};
export default WebGame;
