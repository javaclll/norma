import "./App.css";
import Board from "./components/Board/Board.jsx";

import { GameProvider } from "./context/GameContext";

function App() {
  return (
    <GameProvider>
      <Board />
    </GameProvider>
  );
}

export default App;
