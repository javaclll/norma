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


// export const startingLayout = [
//   [1, 1, 1, 1, 1],
//   [1, 1, 1, 1, 1],
//   [1, 1, 1, 1, 1],
//   [1, 1, 0, 0, 0],
//   [-1, -1, -1, 0, -1],
// ];

export const GameProvider = ({ children }) => {
  const [turn, setTurn] = useState(ItemTypes.GOAT);

  const [goatCounter, setGoatCounter] = useState(0);

  const [moveCounter, setMoveCounter] = useState(0);

  const [goatsCaptured, setGoatsCaptured] = useState(0);

  const [gameResult, setGameResult] = useState({ decided: false });

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

  const gameStatusCheck = (position, capturedThisRound) => {
    if (goatsCaptured + (capturedThisRound ? 1 : 0) >= 6) {
      return { decided: true, wonBy: -1 };
    }

    let tigerHasMove = (() => {
      for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
          if (position[i][j] === -1) {
            for (let k = -2; k <= 2; k++) {
              for (let l = -2; l <= 2; l++) {
                let thisPieceHasAMove = checkMove(
                  {
                    source: [i, j],
                    target: [i + k, j + l],
                  },
                  position,
                  ItemTypes.TIGER
                );
                if (thisPieceHasAMove["isValid"]) {
                  return true;
                }
              }
            }
          }
        }
      }
      return false;
    })();

    if (!tigerHasMove) {
      return { decided: true, wonBy: 1 };
    }

    return { decided: false };
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

      let gameStatusAfterMove = gameStatusCheck(
        new_state,
        eval_move["isCaptureMove"]
      );
      if (gameStatusAfterMove.decided === true) {
        setGameResult(gameStatusAfterMove);
      }

      setGame(new_state);
      setMoveCounter(moveCounter + 1);
    }
  };

  const placeGoat = ({ target: [m, n] }) => {
    if (game[m][n] !== 0 || gameResult.decided) {
      return false;
    } else {
      let new_state = [...game];

      let new_history = JSON.parse(JSON.stringify(moveHistory));
      new_history.push(game);

      setMoveHistory(new_history);

      setMoveCounter(moveCounter + 1);

      new_state[m][n] = 1;

      let gameStatusAfterMove = gameStatusCheck(new_state, false);
      if (gameStatusAfterMove.decided === true) {
        setGameResult(gameStatusAfterMove);
      }

      setGame(new_state);
      setGoatCounter(goatCounter + 1);
      setTurn(ItemTypes.TIGER);
    }
  };

  const checkMove = (
    { source: [x, y], target: [m, n] },
    position = game,
    assumingTurn = turn
  ) => {
    if (x < 0 || y < 0 || m < 0 || n < 0 || x > 4 || y > 4 || m > 4 || n > 4) {
      console.log(`Reason 1`)
      return { isValid: false };
    }

    if (gameResult.decided) {
      console.log(`Reason 2`)
      return { isValid: false };
    }

    if (moveCounter + 1 !== moveHistory.length) {
      console.log(`Reason 3, Move count: ${moveHistory.length} ${moveCounter}`)
      return { isValid: false };
    }

    // Is piece moved in its own turn
    if (
      !(
        (assumingTurn === ItemTypes.GOAT && position[x][y] === 1) ||
        (assumingTurn === ItemTypes.TIGER && position[x][y] === -1)
      )
    ) {
      console.log(`Reason 4`)
      return { isValid: false };
    }

    // Can't move goat before all goats are placed
    if (assumingTurn === ItemTypes.GOAT) {
      if (goatCounter < 20) {
        console.log(`Reason 5`)
        return { isValid: false };
      }
    }

    // If target has some piece
    if (position[m][n] !== 0) {
      console.log(`Reason 6`)
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
      console.log(`Reason 7`)
      return { isValid: false };
    }

    // Tiger can jump goats
    if (   // (2,0), (2,2), (0, 2), (2, 2)
      assumingTurn === ItemTypes.TIGER &&
      ((xDiffAbs === 2 && yDiffAbs === 0 ) ||
        (yDiffAbs === 2 && (xDiffAbs === 0 || xDiffAbs === 2)))
    ) {
      if(xDiffAbs === 2 && yDiffAbs === 2){
        if (sSum%2 !== 0){
          console.log(`Reason 13`)
          return { isValid: false }
        }

      }
      let pieceToCapture = [x + xDiff / 2, y + yDiff / 2];

      //Check if piece to capture is goat
      if (position[pieceToCapture[0]][pieceToCapture[1]] === 1) {
        console.log(`Reason 8`)
        return {
          isValid: true,
          isCaptureMove: true,
          capturePiece: pieceToCapture,
        };
      } else {
        console.log(`Reason 9`)
        return { isValid: false };
      }
    }

    // Can't move distance more than 2
    if (xDiffAbs > 1 || yDiffAbs > 1) {
      console.log(`Reason 10`)
      return { isValid: false };
    }

    // Can't move from odd position to another odd position
    // Example: 0,1 (0+1 = 1 odd) to 1,2 (1+2 = 3 odd)
    else if (sSum % 2) {
      if (tSum % 2) {
        console.log(`Reason 11`)
        return { isValid: false };
      }
    }

    console.log(`Reason 12`)
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
    gameResult,
  };

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>;
};
