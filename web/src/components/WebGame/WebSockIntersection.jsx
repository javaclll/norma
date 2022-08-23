import { useDrop } from "react-dnd";
import { useContext, useState, useEffect } from "react";
import { ItemTypes } from "../../utils/config.jsx";
import { OnlineGameContext } from "../../context/OnlineGameContext";
import { WebsocketContext } from "../../utils/WebSocketContext";

export const WebSockIntersection = ({ x, y, children }) => {
  const {
    game,
    makeMove,
    checkMove,
    turn,
    goatCounter,
    placeGoat,
    moveHistory,
    goatsCaptured,
  } = useContext(OnlineGameContext);

  const cordToPGN = ({ source: [x, y], target: [m, n] }) => {
    let secondChar = x === "X" ? x : (5 - parseInt(x)).toString();
    let fourthChar = m === "X" ? m : (5 - parseInt(m)).toString();
    // let fourthChar = m.toString();

    let [firstChar, thirdChar] = [y, n].map((item) => {
      switch (parseInt(item)) {
        case 0:
          return "A";
        case 1:
          return "B";
        case 2:
          return "C";
        case 3:
          return "D";
        case 4:
          return "E";
        default:
          return "X";
      }
    });
    return firstChar + secondChar + thirdChar + fourthChar;
  };

  useEffect(() => {
    console.log(turn + "bhitrta bata");
  }, [turn]);

  const [{ isOver, canDrop }, drop] = useDrop(
    () => ({
      accept: [ItemTypes.TIGER, ItemTypes.GOAT],
      canDrop: (item) => {
        return checkMove({
          source: item["location"],
          target: [x, y],
        }).isValid;
      },

      drop: (item) => {
        const currentPGN = cordToPGN({
          source: item["location"],
          target: [x, y],
        });
        websocket.send(JSON.stringify({ type: 1, move: currentPGN }));
        // makeMove({
        //   source: item["location"],
        //   target: [x, y],
        // });
      },
      collect: (monitor) => {
        return {
          isOver: !!monitor.isOver(),
          canDrop: !!monitor.canDrop(),
        };
      },
    }),
    [game, moveHistory.length, goatCounter, goatsCaptured]
  );
  const websocket = useContext(WebsocketContext);

  const onClickHandler = () => {
    if (turn == ItemTypes.GOAT && goatCounter < 20) {
      const currentPGN = cordToPGN({ source: ["X", "X"], target: [x, y] });
      websocket.send(JSON.stringify({ type: 1, move: currentPGN }));
    }
  };

  return (
    <td
      ref={drop}
      role="Space"
      className="cell"
      onClick={() => onClickHandler()}
    >
      {children}
    </td>
  );
};

export default WebSockIntersection;
