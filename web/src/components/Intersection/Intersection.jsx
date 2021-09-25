import { useDrop } from "react-dnd";
import {useContext} from "react";
import { ItemTypes } from "../../utils/config.jsx";
import { GameContext } from "../../context/GameContext";

export const Intersection = ({ x, y, children}) => {
  const {game, makeMove} = useContext(GameContext);
  const [{ isOver, canDrop }, drop] = useDrop(
    () => ({
      accept: ItemTypes.TIGER,
      canDrop: () => true,
      drop: (item) => {
          makeMove({source:item["location"], target:[x,y]});
      },
      collect: (monitor) => {
      return {
        isOver: !!monitor.isOver(),
        canDrop: !!monitor.canDrop(),
      }},
    }),
    [game]
  );
  return (
    <td ref={drop} role="Space" className="cell">
      {children}
    </td>
  );
};

export default Intersection;
