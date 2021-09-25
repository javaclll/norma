import { ItemTypes } from "../utils/config";

export class Game {
  gameState = [
    [-1, 0, 0, 0, -1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [-1, 0, 0, 0, -1],
  ];
  goatPlaceCount = 0;
  observers = [];

  allGoatsPlaced() {
    return this.goatPlaceCount === 20;
  }

  observe(o) {
    this.observers.push(o);
    this.emitChange();
    return () => {
      this.observers = this.observers.filter((t) => t !== o);
    };
  }

  move({from, to}) {
    console.log(this.gameState);
    this.gameState[to[0]][to[1]] = this.gameState[from[0]][from[1]];
    this.gameState[from[0]][from[1]] = 0;
    this.emitChange();
  }

  emitChange() {
    const pos = this.gameState;
    this.observers.forEach((o) => o && o(pos));
  }
}
