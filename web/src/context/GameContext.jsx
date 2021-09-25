import { createContext, useState } from "react";
import { ItemTypes } from "../utils/config";

export const GameContext = createContext(null);

export const GameProvider = ({ children }) => {
  const [turn, setTurn] = useState(ItemTypes.GOAT);
  const [game, setGame] = useState([
    [-1, 0, 0, 0, -1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [-1, 0, 0, 0, -1],
  ]);

  const makeMove = ({ source, target }) => {
    let new_state = [...game];
    new_state[target[0]][target[1]] = new_state[source[0]][source[1]];
    new_state[source[0]][source[1]] = 0;
    setGame(new_state);
  };

  const value = {
    turn,
    setTurn,
    game,
    setGame,
    makeMove,
  };

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>;
};
