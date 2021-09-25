import { DndProvider } from "react-dnd";
import { useEffect, useState, useContext } from "react";
import { HTML5Backend } from "react-dnd-html5-backend";
import board from "../../statics/board.svg";
import CoRe from "../Common/ConditionalRendering";
import Goat from "../Goat/Goat.jsx";
import Intersection from "../Intersection/Intersection.jsx";
import Tiger from "../Tiger/Tiger.jsx";
import { GameContext } from "../../context/GameContext";

const Board = () => {
  const {game} = useContext(GameContext);
  return (
    <DndProvider backend={HTML5Backend}>
    {console.log(game)}
      <div className="board" style={{ backgroundImage: `url(${board})` }}>
        <div className="tableDiv">
          <table className="boardTable">

            {game.map((row, rowIndex) => (
              <tr className="row">
                {row.map((value, colIndex) => (
                  <Intersection x={rowIndex} y={colIndex}>
                    <CoRe condition={value === 1}>
                      <Goat m={rowIndex} n={colIndex}/>
                    </CoRe>
                    <CoRe condition={value === 0}>{null}</CoRe>
                    <CoRe condition={value === -1}>
                      <Tiger m={rowIndex} n={colIndex}/>
                    </CoRe>
                  </Intersection>
                ))}
              </tr>
            ))}
          </table>
        </div>
      </div>
    </DndProvider>
  );
};
export default Board;
