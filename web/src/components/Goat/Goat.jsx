import goat from "../../statics/goat.svg";
import "./styles/goat.css";
import { ItemTypes } from "../../utils/config.jsx";
import { useDrag } from "react-dnd";

const Goat = () => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: ItemTypes.GOAT,
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }));
  return (
    <div
      className="goatDiv"
      ref={drag}
      style={{
        opacity: isDragging ? 0.5 : 1,
        fontSize: 25,
        fontWeight: "bold",
        cursor: "move",
      }}
    >
      <img src={goat} />
    </div>
  );
};
export default Goat;
