import goat from "../../statics/goat.svg";
import "./styles/goat.css";
import { ItemTypes } from "../../utils/config.jsx";
import { useDrag, DragPreviewImage } from "react-dnd";

const Goat = ({ m, n }) => {
  const [{ isDragging }, drag, preview] = useDrag(() => ({
    item: {
      location: [m, n],
    },
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
        cursor: "grab",
      }}
    >
      <DragPreviewImage connect={preview} src={null} />
      <img src={goat} />
    </div>
  );
};
export default Goat;
