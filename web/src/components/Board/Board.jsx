import { DndProvider } from "react-dnd";
import { useContext } from "react";
import { HTML5Backend } from "react-dnd-html5-backend";
import board from "../../statics/board.svg";
import CoRe from "../Common/ConditionalRendering";
import Goat from "../Goat/Goat.jsx";
import Intersection from "../Intersection/Intersection.jsx";
import Tiger from "../Tiger/Tiger.jsx";
import { GameContext } from "../../context/GameContext";
import { ItemTypes } from "../../utils/config";
import arrow from "../../statics/arrow.svg";

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
  } = useContext(GameContext);
  return (
    <>
      <DndProvider backend={HTML5Backend}>
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
      </DndProvider>

      <div className="right-box">
        <div className="button-panel">
          <button
            className="backward button"
            onClick={previousMove}
            disabled={moveCounter === 0}
          >
            <img className="arrow" src={arrow} />
          </button>
          <div className="move-number">{moveCounter}</div>
          <button
            className="forward button"
            onClick={nextMove}
            disabled={moveCounter === moveHistory.length - 1}
          >
            <img className="arrow" src={arrow} />
          </button>
        </div>

        <div className="detail-box">
          <CoRe condition={!gameResult.decided}>
            <h2>{turn === ItemTypes.GOAT ? "Goat" : "Tiger"}'s Turn</h2>
          </CoRe>
          <CoRe condition={gameResult.decided}>
            <h2>{gameResult.wonBy===-1?"Tiger":"Goat"} Won!</h2>
          </CoRe>
          <h2>Captured Goats: {goatsCaptured}</h2>
          <h2>Placed Goats: {goatCounter}</h2>
        </div>
      </div>
    </>
  );
};
export default Board;
