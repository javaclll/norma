import tiger from "../../statics/tiger.svg";
import "./styles/tiger.css";
import { ItemTypes } from "../../utils/config.jsx";
import { useDrag, DragPreviewImage } from "react-dnd";

const Tiger = ({ m, n}) => {
  const [{ isDragging }, drag, preview] = useDrag(() => ({
    item: {
      location: [m, n],
    },
    type: ItemTypes.TIGER,
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }));
  return (
    <div
      className="tigerDiv"
      ref={drag}
      style={{
        opacity: isDragging ? 0.5 : 1,
        cursor: "grab",
      }}
    >
      <DragPreviewImage connect={preview} src={null} />
      <img src={tiger} />
    </div>
  );
};
export default Tiger;
