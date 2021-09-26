import { createContext, useState } from "react";
import { ItemTypes } from "../utils/config";

export const GameContext = createContext(null);

export const startingLayout = [
  [-1, 0, 0, 0, -1],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [-1, 0, 0, 0, -1],
];

export const GameProvider = ({ children }) => {
  const [turn, setTurn] = useState(ItemTypes.GOAT);

  const [goatCounter, setGoatCounter] = useState(0);

  const [moveCounter, setMoveCounter] = useState(0);

  const [goatsCaptured, setGoatsCaptured] = useState(0);

  const [moveHistory, setMoveHistory] = useState([startingLayout]);

  const [game, setGame] = useState(startingLayout);

  const nextMove = () => {
    setGame(moveHistory[moveCounter + 1]);
    setMoveCounter(moveCounter + 1);
  };

  const previousMove = () => {
    setGame(moveHistory[moveCounter - 1]);
    setMoveCounter(moveCounter - 1);
  };

  const makeMove = ({ source: [x, y], target: [m, n] }) => {
    let eval_move = checkMove({ source: [x, y], target: [m, n] });

    if (eval_move["isValid"]) {
      let new_state = [...game];

      let new_history = JSON.parse(JSON.stringify(moveHistory));
      new_history.push(game);
      setMoveHistory(new_history);

      if (eval_move["isCaptureMove"]) {
        new_state[eval_move["capturePiece"][0]][
          eval_move["capturePiece"][1]
        ] = 0;
        setGoatsCaptured(goatsCaptured + 1);
      }

      new_state[m][n] = new_state[x][y];
      new_state[x][y] = 0;
      turn === ItemTypes.GOAT
        ? setTurn(ItemTypes.TIGER)
        : setTurn(ItemTypes.GOAT);
      setGame(new_state);
      setMoveCounter(moveCounter + 1);
    }
  };

  const placeGoat = ({ target: [m, n] }) => {
    if (game[m][n] !== 0) {
      return false;
    } else {
      let new_state = [...game];

      let new_history = JSON.parse(JSON.stringify(moveHistory));
      new_history.push(game);
      setMoveHistory(new_history);

      setMoveCounter(moveCounter + 1);
      new_state[m][n] = 1;
      setGame(new_state);
      setGoatCounter(goatCounter + 1);
      setTurn(ItemTypes.TIGER);
    }
  };

  const checkMove = ({ source: [x, y], target: [m, n] }) => {
    // if(moveCounter != moveHistory.length -1){
    //     return false;
    // }

    // Is piece moved in its own turn
    if (
      !(
        (turn === ItemTypes.GOAT && game[x][y] === 1) ||
        (turn === ItemTypes.TIGER && game[x][y] === -1)
      )
    ) {
      return { isValid: false };
    }

    // Can't move goat before all goats are placed
    if (turn === ItemTypes.GOAT) {
      if (goatCounter < 20) {
        return { isValid: false };
      }
    }

    // If target has some piece
    if (game[m][n] !== 0) {
      return { isValid: false };
    }

    let xDiffAbs = Math.abs(x - m);
    let yDiffAbs = Math.abs(y - n);
    let xDiff = m - x;
    let yDiff = n - y;
    let sSum = x + y;
    let tSum = m + n;

    // Source and target can't be same
    if (xDiffAbs === 0 && yDiffAbs === 0) {
      return { isValid: false };
    }

    // Tiger can jump goats
    if (
      turn === ItemTypes.TIGER &&
      ((xDiffAbs === 2 && (yDiffAbs === 0 || yDiffAbs === 2)) ||
        (yDiffAbs === 2 && (xDiffAbs === 0 || xDiffAbs === 2)))
    ) {
      let pieceToCapture = [x + xDiff / 2, y + yDiff / 2];

      //Check if piece to capture is goat
      if (game[pieceToCapture[0]][pieceToCapture[1]] === 1) {
        return {
          isValid: true,
          isCaptureMove: true,
          capturePiece: pieceToCapture,
        };
      } else {
        return { isValid: false };
      }
    }

    // Can't move distance more than 2
    if (xDiffAbs > 1 || yDiffAbs > 1) {
      return { isValid: false };
    }

    // Can't move from odd position to another odd position
    // Example: 0,1 (0+1 = 1 odd) to 1,2 (1+2 = 3 odd)
    else if (sSum % 2) {
      if (tSum % 2) {
        return { isValid: false };
      }
    }

    return { isValid: true, isCaptureMove: false };
  };

  const value = {
    turn,
    setTurn,
    game,
    setGame,
    makeMove,
    placeGoat,
    checkMove,
    goatCounter,
    goatsCaptured,
    nextMove,
    previousMove,
    moveCounter,
    moveHistory,
  };

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>;
};
