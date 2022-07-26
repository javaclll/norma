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
import arrow from "../../statics/arrow.svg";
import "../Board/styles/board.css";
import tiger from "../../statics/tiger.svg";
import goat from "../../statics/goat.svg";
import replay from "../../statics/replay.svg";

const Analysis = () => {
  const {
    game,
    setGame,
    gameResult,
    turn,
    setTurn,
    goatsCaptured,
    setGoatsCaptured,
    goatCounter,
    nextMove,
    previousMove,
    moveCounter,
    moveHistory,
    setMoveHistory,
    playFromThisPoint,
    setGoatCounter,
    pgn,
    setPGN,
    cordToPGN,
    startingLayout,
    setGameResult,
    setMoveCounter,
    checkMove,
    gameStatusCheck,
    gameStatusAfterMove,
  } = useContext(GameContext);

  const onClickHandler = () => {
    window.location = window.location;
  };

  const handlePGNLoad = (e) => {
    var PGNList = LoadPGN.split("-");
    PGNList = PGNList.map((data) => data.replace(/\s/g, ""));
    var CordList = [];

    let new_state = [
      [-1, 0, 0, 0, -1],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [-1, 0, 0, 0, -1],
    ];
    // let new_history = cloneDeep(moveHistory);
    //start
    var tempTurn = ItemTypes.GOAT;
    var goatsCap = 0;
    var goatsPlace = 0;
    var tempHistory = [
      {
        game: startingLayout,
        goatCount: 0,
        goatsCaptured: 0,
      },
    ];
    var tempPGN = [];
    for (var i = 0; i < PGNList.length; i++) {
      if (i % 2 == 0) {
        tempTurn = ItemTypes.GOAT;
      } else {
        tempTurn = ItemTypes.TIGER;
      }

      const temp = PGNList[i].split("");
      const temp2 = PGNtoCord({
        source: [temp[0], temp[1]],
        target: [temp[2], temp[3]],
      });

      const finalcut = temp2.split("");
      if (finalcut[0] == "X") {
        new_state[finalcut[2]][finalcut[3]] = 1;
        goatsPlace++;
      } else {
        const eval_move = PGNHelper(
          {
            source: [parseInt(finalcut[0]), parseInt(finalcut[1])],
            target: [parseInt(finalcut[2]), parseInt(finalcut[3])],
          },
          new_state,
          tempTurn
        );
        if (eval_move["isValid"]) {
          let captured = eval_move["isCaptureMove"];
          if (captured) {
            new_state[eval_move["capturePiece"][0]][
              eval_move["capturePiece"][1]
            ] = 0;
            goatsCap++;
          }
          new_state[finalcut[2]][finalcut[3]] =
            new_state[finalcut[0]][finalcut[1]];
          new_state[finalcut[0]][finalcut[1]] = 0;

          // let gameStatusAfterMove = gameStatusCheck(
          //   new_state,
          //   eval_move["isCaptureMove"]
          // );
          // if (gameStatusAfterMove.decided === true) {
          //   setGameResult(gameStatusAfterMove);
          // }
        }
      }

      tempPGN.push(
        cordToPGN({
          source: [finalcut[0], finalcut[1]],
          target: [finalcut[2], finalcut[3]],
        })
      );

      var tempHistoryObject = {
        game: new_state,
        goatCount: goatsPlace,
        goatsCaptured: goatsCap,
      };
      var t = cloneDeep(tempHistory);
      t.push(tempHistoryObject);
      tempHistory = cloneDeep(t);
      // console.log("new + " + new_state);
      // console.log(tempHistory);
    }
    tempTurn == ItemTypes.GOAT
      ? (tempTurn = ItemTypes.TIGER)
      : (tempTurn = ItemTypes.GOAT);
    setGame(new_state);
    let gameStatusAfterMove = pgnStatusCheck(new_state, goatsCap, goatsPlace);
    if (gameStatusAfterMove.decided === true) {
      setGameResult(gameStatusAfterMove);
    }
    setPGN([...tempPGN]);
    setGoatsCaptured(goatsCap);
    setGoatCounter(goatsPlace);
    setMoveHistory(tempHistory);
    setMoveCounter(PGNList.length);
    console.log(tempTurn);
    setTurn(tempTurn);
  };

  const pgnStatusCheck = (position, goatsCap, goatsPlace) => {
    if (goatsCap >= 6) {
      return { decided: true, wonBy: -1 };
    }

    let tigerHasMove = (() => {
      for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
          if (position[i][j] === -1) {
            for (let k = -2; k <= 2; k++) {
              for (let l = -2; l <= 2; l++) {
                let thisPieceHasAMove = checkMove(
                  {
                    source: [i, j],
                    target: [i + k, j + l],
                  },
                  position,
                  ItemTypes.TIGER
                );
                if (thisPieceHasAMove["isValid"]) {
                  return true;
                }
              }
            }
          }
        }
      }
      return false;
    })();

    let goatHasMove = (() => {
      for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
          if (position[i][j] === 1) {
            for (let k = -2; k <= 2; k++) {
              for (let l = -2; l <= 2; l++) {
                let thisPieceHasAMove = checkMove(
                  {
                    source: [i, j],
                    target: [i + k, j + l],
                  },
                  position,
                  ItemTypes.GOAT
                );
                if (thisPieceHasAMove["isValid"]) {
                  return true;
                }
              }
            }
          }
        }
      }
      return false;
    })();

    if (!goatHasMove) {
      if (goatsPlace != 20) {
        console.log(goatsPlace);
        goatHasMove = true;
      }
    }

    if (turn == ItemTypes.GOAT) {
      console.log("hi tiuger");
      if (!goatHasMove) {
        return { decided: true, wonBy: -1 };
      }
    } else if (turn == ItemTypes.TIGER) {
      if (!tigerHasMove) {
        console.log("hi goat");
        return { decided: true, wonBy: 1 };
      }
    }

    return { decided: false };
  };

  const PGNHelper = (
    { source: [x, y], target: [m, n] },
    position,
    assumingTurn
  ) => {
    let xDiffAbs = Math.abs(x - m);
    let yDiffAbs = Math.abs(y - n);
    let xDiff = m - x;
    let yDiff = n - y;
    let sSum = x + y;
    let tSum = m + n;

    // Tiger can jump goats
    if (
      // (2,0), (2,2), (0, 2), (2, 2)
      assumingTurn === ItemTypes.TIGER &&
      ((xDiffAbs === 2 && yDiffAbs === 0) ||
        (yDiffAbs === 2 && (xDiffAbs === 0 || xDiffAbs === 2)))
    ) {
      let pieceToCapture = [x + xDiff / 2, y + yDiff / 2];
      if (position[pieceToCapture[0]][pieceToCapture[1]] === 1) {
        const reason = "Can capture goat!";
        return {
          isValid: true,
          isCaptureMove: true,
          capturePiece: pieceToCapture,
          reason: reason,
        };
      } else {
        const reason = "Cannot capture tiger!";
        return { isValid: false, reason: reason };
      }
    }

    // Can't move distance more than 2
    if (xDiffAbs > 1 || yDiffAbs > 1) {
      const reason = "Cannot move distance more than 2!";
      return { isValid: false, reason: reason };
    } // Can't move from odd position to another odd position
    // Example: 0,1 (0+1 = 1 odd) to 1,2 (1+2 = 3 odd)
    else if (sSum % 2) {
      if (tSum % 2) {
        const reason = "Can't move from odd position to another odd position!";
        return { isValid: false, reason: reason };
      }
    }

    const reason = "Default move!";
    return { isValid: true, isCaptureMove: false, reason: reason };
  };

  const [LoadPGN, setLoadPGN] = useState("");

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
              <div className="a_copyButtonBox">
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
            <div className="pgn_form">
              <form>
                <textarea
                  placeholder="PGN"
                  className="load_PGN"
                  value={LoadPGN}
                  onChange={(e) => setLoadPGN(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      e.stopPropagation();
                      handlePGNLoad();
                    }
                  }}
                />

                <div className="a_submitButtonBox">
                  {notifShow ? (
                    <a className="c_Notif">Copied to Clipboard</a>
                  ) : (
                    ""
                  )}
                  <button
                    className="copyButton"
                    type="button"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      handlePGNLoad();
                    }}
                  >
                    <a className="copy_text">Submit</a>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </DndProvider>
    </>
  );
};
export default Analysis;
