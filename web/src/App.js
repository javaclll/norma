import "./App.css";
import Board from "./components/Board/Board.jsx";
import StartScreen from "./components/StartScreen/StartScreen.jsx";
import Analysis from "./components/Analysis/Analysis.jsx";
import NormaPlay from "./components/NormaPlay/NormaPlay.jsx";
import Online from "./components/Online/Online.jsx";
import WebGame from "./components/WebGame/WebGame.jsx";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { GameProvider } from "./context/GameContext";
import { OnlineGameProvider } from "./context/OnlineGameContext";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<StartScreen />} />
        <Route
          path="/game"
          element={
            <GameProvider>
              <Board />
            </GameProvider>
          }
        />
        <Route path="/online" element={<Online />} />
        <Route
          path="/play"
          element={
            <OnlineGameProvider>
              <WebGame />
            </OnlineGameProvider>
          }
        />
        <Route
          path="/analysis"
          element={
            <GameProvider>
              <Analysis />
            </GameProvider>
          }
        />
        <Route
          path="/norma"
          element={
            <GameProvider>
              <NormaPlay />
            </GameProvider>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
