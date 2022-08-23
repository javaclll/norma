import { DndProvider } from "react-dnd";
import { useContext, useState } from "react";
import { HTML5Backend } from "react-dnd-html5-backend";
import { GameContext } from "../../context/GameContext";
import { ItemTypes } from "../../utils/config";
import { Link } from "react-router-dom";
import "./styles/start.css";
import tiger from "../../statics/tiger.svg";
import goat from "../../statics/goat.svg";

const StartScreen = () => {
  const onClickHandler = () => {
    window.location = "/";
  };

  const [notifShow, setNotif] = useState(false);

  return (
    <>
      <DndProvider backend={HTML5Backend}>
        <div className="menu-main-container">
          <div className="menu">
            <img src={tiger} className="start_image" />
            <img src={goat} className="start_image" />
          </div>
          <div className="start-menu-text">
            <a className="menu-big">Baghchal</a>
          </div>
          <div className="start-menu-buttons">
            <Link to="/game">
              <button
                className="menuButton button_color1"
                type="button"
                onClick={(e) => {}}
              >
                <a className="menu_text">Play Offline</a>
              </button>
            </Link>
            <Link to="/online">
              <button
                className="menuButton button_color2"
                type="button"
                onClick={(e) => {}}
              >
                <a className="menu_text">Play Online</a>
              </button>
            </Link>
            <Link to="/analysis">
              <button
                className="menuButton button_color3"
                type="button"
                onClick={(e) => {}}
              >
                <a className="menu_text">Play with Norma</a>
              </button>
            </Link>
            <Link to="/analysis">
              <button
                className="menuButton button_color4"
                type="button"
                onClick={(e) => {}}
              >
                <a className="menu_text">Analysis Board</a>
              </button>
            </Link>
          </div>
          <div className="start-menu-text-bot">
            <a className="menu-small">Powered by Norma</a>
            <a className="menu-small">by AARYA</a>
          </div>
        </div>
      </DndProvider>
    </>
  );
};
export default StartScreen;
