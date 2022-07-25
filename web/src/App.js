import "./App.css";
import Board from "./components/Board/Board.jsx";
import Analysis from "./components/Analysis/Analysis.jsx";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import { GameProvider } from "./context/GameContext";

function App() {
  return (
    <GameProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Board />} />
          <Route path="/analysis" element={<Analysis />} />
        </Routes>
      </BrowserRouter>
    </GameProvider>
  );
}

export default App;
