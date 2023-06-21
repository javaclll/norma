# import torch
from libbaghchal import Baghchal, GameStatus, GameStateInstance, GameStatusCheckResult
from time import sleep

import torch
from torch.cuda import random
from torch.nn.modules.activation import F

from src.models import BaghchalActorCritic

# print(f"GPU Available: {torch.cuda.is_available()}")
# print(f"Device Count: {torch.cuda.device_count()}")


def make_random_move(game: Baghchal):
    possible_moves = game.get_possible_moves()
    move = possible_moves[0]
    game.make_move(move.move[1], move.move[0], None)


def print_board(game: Baghchal):
    board = game.board()
    for row in board:
        print(row)


def play_game(model: BaghchalActorCritic):
    while True:
        for _ in range(512):
            g = Baghchal.default()

            g.set_game_over_on_invalid(state=True)

            # g.set_rewards(
            #     t_goat_capture=0.6,
            #     t_got_trapped=-0.4,
            #     t_trap_escape=0.3,
            #     t_win=1.0,
            #     t_lose=-1.0,
            #     t_draw=0.0,
            #     t_move=0.0,
            #     g_goat_captured=-0.6,
            #     g_tiger_trap=0.6,
            #     g_tiger_escape=-0.3,
            #     g_win=1.0,
            #     g_lose=-1.0,
            #     g_draw=0.0,
            #     g_move=0.0,
            #     gt_invalid_move=-100,
            # )
            g.set_rewards(
                t_goat_capture=0.0,
                t_got_trapped=-0.0,
                t_trap_escape=0.0,
                t_win=0.0,
                t_lose=-0.0,
                t_draw=0.0,
                t_move=0.0,
                g_goat_captured=-0.0,
                g_tiger_trap=0.0,
                g_tiger_escape=-0.0,
                g_win=0.0,
                g_lose=-0.0,
                g_draw=0.0,
                g_move=0.0,
                gt_invalid_move=-0.0,
            )
            g.set_game_over_on_invalid(False)

            while g.game_state() == GameStatus.NotDecided:
                state = g.state_as_inputs_all_symmetry()[0][0]

                action_probs = model.forward_actor(state)

                # action_probs = F.softmax(action_logits, dim=-1)
                action_dist = torch.distributions.Categorical(action_probs)

                action = action_dist.sample()

                transition = g.make_move_index(int(action))

                if transition:
                    print(f"{transition.move}")
                    loss = model.train_step(transition)  # type: ignore
                    print(loss)

                    new_action_probs = model.forward_actor(state)

                    # action_probs = F.softmax(action_logits, dim=-1)
                    print(f"After: {(action_probs - new_action_probs).abs().sum()}")
                else:
                    print(f"No trnasition for action {action}")

            print(f"MoveCount: {g.move_count()}")
            print(f"Game: {g.pgn()}")
            torch.save(model, "state/model.pt")


if __name__ == "__main__":
    try:
        model = torch.load("state/model.pt")
    except Exception as e:
        model = BaghchalActorCritic()

    model.cuda()

    play_game(model)

    torch.save(model, "state/model.pt")
