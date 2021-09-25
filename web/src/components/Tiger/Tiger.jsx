import tiger from "../../statics/tiger.svg";
import "./styles/tiger.css";
import { ItemTypes } from "../../utils/config.jsx";
import { useDrag } from "react-dnd";

const Tiger = ({ m, n }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    item: {
      location: [m, n],
    },
    type: ItemTypes.TIGER,
    collect: (monitor) => {
      return {
        isDragging: !!monitor.isDragging(),
      };
    },
  }));
  return (
    <div
      className="tigerDiv"
      ref={drag}
      style={{
        opacity: isDragging ? 0.5 : 1,
        fontSize: 25,
        fontWeight: "bold",
        cursor: "move",
      }}
    >
      <img src={tiger} />
    </div>
  );
};
export default Tiger;
