from typing import List


def state_printer(arr: List[int]) -> None:
    labels = [
        "Goat Board",
        "Tiger Board",
        "Empty Space Board",
        "Source Board",
        "Destination Board",
    ]
    for i in range(5):
        board = arr[i * 25 : (i + 1) * 25]
        for j, val in enumerate(board):
            if val == 0:
                board[j] = " - "  # type: ignore
            elif val == 1:
                board[j] = " X "  # type: ignore
            else:
                board[j] = " O "  # type: ignore
        print(f"{labels[i]}:")
        print("\n".join(["".join(row) for row in [board[5 * j : 5 * (j + 1)] for j in range(5)]]))  # type: ignore
        print("\n")

    goat_placement_complete = arr[125]
    goats_captured = arr[126:130]
    turn = arr[130]
    print(f"Goat Placement Complete: {goat_placement_complete}")
    print(f"Goats Captured: {goats_captured}")
    print(f"Turn: {turn}")
