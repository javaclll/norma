import { useDrop } from "react-dnd";
import { useContext } from "react";
import { ItemTypes } from "../../utils/config.jsx";
import { GameContext } from "../../context/GameContext";

export const Intersection = ({ x, y, children }) => {
  const {
    game,
    makeMove,
    checkMove,
    turn,
    goatCounter,
    placeGoat,
    moveHistory,
  } = useContext(GameContext);

  const [{ isOver, canDrop }, drop] = useDrop(
    () => ({
      accept: [ItemTypes.TIGER, ItemTypes.GOAT],
      canDrop: (item) =>
        checkMove(
          { source: item["location"], target: [x, y] },
          () => (moveHistory),
        ).isValid,
      drop: (item) => {
        makeMove({ source: item["location"], target: [x, y] });
      },
      collect: (monitor) => {
        return {
          isOver: !!monitor.isOver(),
          canDrop: !!monitor.canDrop(),
        };
      },
    }),
    [game, moveHistory.length],
  );

  const onClickHandler = () => {
    if (turn == ItemTypes.GOAT && goatCounter < 20) {
      placeGoat({ target: [x, y] });
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

export default Intersection;
