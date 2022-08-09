import { DndProvider } from "react-dnd";
import { useContext, useState } from "react";
import { HTML5Backend } from "react-dnd-html5-backend";
import board from "../../statics/board.svg";
import CoRe from "../Common/ConditionalRendering";
import Goat from "../Goat/Goat.jsx";
import Intersection from "../Intersection/Intersection.jsx";
import Tiger from "../Tiger/Tiger.jsx";
import { GameContext } from "../../context/GameContext";
import { ItemTypes } from "../../utils/config";
import { cloneDeep } from "lodash";
import { Link } from "react-router-dom";
import arrow from "../../statics/arrow.svg";
import "../Board/styles/board.css";
import tiger from "../../statics/tiger.svg";
import goat from "../../statics/goat.svg";
import replay from "../../statics/replay.svg";

const Board = () => {
  const {
    game,
    gameResult,
    turn,
    goatsCaptured,
    goatCounter,
    nextMove,
    previousMove,
    moveCounter,
    moveHistory,
    playFromThisPoint,
    pgn,
  } = useContext(GameContext);

  const onClickHandler = () => {
    window.location = "/";
  };

  const [notifShow, setNotif] = useState(false);

  return (
    <>
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
                  <h2>{turn === ItemTypes.GOAT ? "Goat" : "Tiger"}'s Turn</h2>
                </CoRe>
                <CoRe condition={gameResult.decided}>
                  <h2>{gameResult.wonBy === -1 ? "Tiger" : "Goat"} Won!</h2>
                </CoRe>
                <h2>Captured Goats: {goatsCaptured}</h2>
                <h2>Placed Goats: {goatCounter}</h2>
                <h2>History Length: {moveHistory.length}</h2>
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
                        <Intersection
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
                        </Intersection>
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
                src={gameResult.wonBy === ItemTypes.GOAT ? tiger : goat}
                className="win-screen-img"
              />
              <a className="win-screen-text">
                {gameResult.wonBy ? "Tiger" : "Goat"} Wins!
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
    </>
  );
};
export default Board;
