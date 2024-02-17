from libbaghchal import Baghchal
from random import shuffle

INF = 1e6


class MiniMax:
    def __init__(self, depth=4):
        self.depth = depth

    def evaluation(self, board, goat_eval=True):
        winner = board.game_state()

        if goat_eval:
            if winner == 1:
                return INF
            elif winner == 2:
                return -INF
            else:
                return 0
        else:
            if winner == 2:
                return INF
            elif winner == 1:
                return -INF
            else:
                return 0

    def goatMax(self, board: Baghchal, depth, maximizing_player=True):
        if depth == 0 or board.game_status_check().decided:
            # print(f'depth: {depth}, player: {maximizing_player}, result: Evaluating')
            return self.evaluation(board, goat_eval=True), None

        if maximizing_player:
            maxValue = -INF
            best_move = None
            possible_moves = board.get_possible_moves()
            # shuffle(possible_moves)
            for i in possible_moves:
                board_cp = board.copy()
                board_cp.make_move(*i.move)
                moveReward = board_cp.move_reward_goat()[-1]

                result = self.goatMax(board_cp, depth - 1, maximizing_player=False)

                reward = result[0] + moveReward

                # print()
                # print()
                # print(f"Goat Move Current {i.move}.")
                # print()
                # print(f"Goat Move for Goat Maximizer at Depth {depth}.")
                # print(f"moveReward: {moveReward}.")
                # print(f"results: {result}.")
                # print(f"total reward: {reward} and maxValue: {maxValue}.")
                if reward > maxValue:
                    maxValue = reward
                    best_move = i.move

                # print(f"new maxValue: {maxValue}.")
                # print()
                # print()
            return maxValue, best_move

        else:
            minValue = INF
            best_move = None
            possible_moves = board.get_possible_moves()

            for i in possible_moves:
                board_cp = board.copy()
                board_cp.make_move(*i.move)
                moveReward = board_cp.move_reward_tiger()[-1]
                result = self.goatMax(board_cp, depth - 1, maximizing_player=True)

                reward = result[0] - moveReward

                # print()
                # print()
                # print(f"Tiger Move Current {i.move}.")
                # print()
                # print(f"Tiger Move for Goat Maximizer at Depth {depth}.")
                # print(f"moveReward: {moveReward}.")
                # print(f"results: {result}.")
                # print(f"total reward: {reward} and minValue: {minValue}.")
                if reward < minValue:
                    minValue = reward
                    best_move = i.move

                # print(f"new minValue: {minValue}.")
                # print()
                # print()
            return minValue, best_move

    def tigerMax(self, board: Baghchal, depth, maximizing_player=True):
        if depth == 0 or board.game_status_check().decided:
            return self.evaluation(board, goat_eval=False), None

        if maximizing_player:
            maxValue = -INF
            best_move = None
            possible_moves = board.get_possible_moves()
            # shuffle(possible_moves)
            for i in possible_moves:
                board_cp = board.copy()
                board_cp.make_move(*i.move)
                moveReward = board_cp.move_reward_tiger()[-1]

                result = self.tigerMax(board_cp, depth - 1, maximizing_player=False)

                reward = (1.5 - depth / 5) * (result[0] + moveReward)

                # print()
                # print()
                # print(f"Tiger Move Current {i.move}.")
                # print()
                # print(f"Tiger Move for Tiger Maximizer at Depth {depth}.")
                # print(f"moveReward: {moveReward}.")
                # print(f"results: {result}.")
                # print(f"total reward: {reward} and maxValue: {maxValue}.")
                if reward > maxValue:
                    maxValue = reward
                    best_move = i.move

                # print(f"new maxValue: {maxValue}.")
                # print()
                # print()
            return maxValue, best_move

        else:
            minValue = INF
            best_move = None
            possible_moves = board.get_possible_moves()
            # shuffle(possible_moves)

            for i in possible_moves:
                board_cp = board.copy()
                board_cp.make_move(*i.move)
                moveReward = board_cp.move_reward_goat()[-1]
                result = self.tigerMax(board_cp, depth - 1, maximizing_player=True)

                reward = (1.5 - depth / 5) * (result[0] - moveReward)

                # print()
                # print()
                # print(f"Goat Move Current {i.move}.")
                # print()
                # print(f"Goat Move for Tiger Maximizer at Depth {depth}.")
                # print(f"moveReward: {moveReward}.")
                # print(f"results: {result}.")
                # print(f"total reward: {reward} and minValue: {minValue}.")
                if reward < minValue:
                    minValue = reward
                    best_move = i.move
                # print(f"new minValue: {minValue}.")
                # print()
                # print()
            return minValue, best_move

    def best_bagh_move(self, board):
        assert not board.game_status_check().decided
        return self.tigerMax(board, self.depth, maximizing_player=True)

    def best_goat_move(self, board):
        assert not board.game_status_check().decided
        return self.goatMax(board, self.depth, maximizing_player=True)

    def best_move(self, board: Baghchal):
        if board.turn() == 1:
            result = self.best_goat_move(board)
        else:
            result = self.best_bagh_move(board)

        # print("The Result is: ", result)
        return result
