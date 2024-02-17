import csv
from operator import indexOf
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


def separate_data(file):
    with open(file, "r") as data:
        reader = csv.reader(data)

        with open("goat.csv", "w") as goat, open("tiger.csv", "w") as tiger:
            goat_writer = csv.writer(goat)
            tiger_writer = csv.writer(tiger)

            goat_writer.writerow(
                [
                    "Norma Agent",
                    "Wins",
                    "Loss",
                    "Draw",
                    "Total Games Played",
                    "Predicted Invalid Moves",
                    "Turns",
                ]
            )
            tiger_writer.writerow(
                [
                    "Norma Agent",
                    "Wins",
                    "Loss",
                    "Draw",
                    "Total Games Played",
                    "Predicted Invalid Moves",
                    "Turns",
                ]
            )

            for row in reader:
                if row[0] == "1":
                    goat_writer.writerow(row)

                if row[0] == "-1":
                    tiger_writer.writerow(row)


def plot_data_tiger():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("tiger.csv")
    data.pop("Predicted Invalid Moves")
    data.pop("Turns")

    wins = data["Wins"][::5]
    loss = data["Loss"][::5]
    draw = data["Draw"][::5]
    time = np.arange(len(wins)) * 5

    plt.plot(
        time,
        wins,
        label="Wins",
        color="grey",
        linestyle="solid",
        markersize=2,
        linewidth=1,
    )
    plt.plot(
        time,
        loss,
        label="Loss",
        color="grey",
        linestyle="dotted",
        markersize=2,
        linewidth=1,
    )

    plt.xlabel("Number of Traninigs")
    plt.ylabel("Number of Games")
    plt.legend()

    plt.savefig("tiger.png", dpi=300, bbox_inches="tight")
    plt.clf()


def plot_data_goat():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("goat.csv")
    x = 12
    wins = data["Wins"]
    wins = [wins[i : i + x] for i in range(0, len(wins), x)]
    wins = [max(z) for z in wins]

    loss = data["Loss"]
    loss = [loss[i : i + x] for i in range(0, len(loss), x)]
    loss = [min(z) for z in loss]

    draw = data["Draw"]
    draw = [draw[i : i + x] for i in range(0, len(draw), x)]
    draw = [max(z) for z in draw]

    time = np.arange(len(wins)) * x

    plt.plot(
        time,
        wins,
        label="Wins",
        color="grey",
        linestyle="solid",
        markersize=2,
        linewidth=1,
    )
    plt.plot(
        time,
        loss,
        label="Loss",
        color="grey",
        linestyle="dotted",
        markersize=2,
        linewidth=1,
    )
    plt.plot(
        time,
        draw,
        label="Draw",
        color="grey",
        linestyle="--",
        markersize=2,
        linewidth=1,
    )

    plt.legend()

    plt.xlabel("Number of Traninigs")
    plt.ylabel("Number of Games")

    plt.savefig("goat.png", dpi=300, bbox_inches="tight")
    plt.clf()


def plot_invalid_moves_goat():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("goat.csv")

    invalid_moves = data["Predicted Invalid Moves"].apply(
        lambda x: [int(i) for i in eval(x)]
    )
    game_length = data["Turns"].apply(lambda x: [int(i) for i in eval(x)])
    average_invalid_moves = []
    for i in range(len(invalid_moves)):
        average_invalid_moves.append(sum(invalid_moves[i]) / sum(game_length[i]))

    print(f"\nMax Average Invalid Moves (Goat): {max(average_invalid_moves)}")
    print(f"Min Average Invalid Moves (Goat): {min(average_invalid_moves)}")

    plt.plot(
        range(len(average_invalid_moves)),
        average_invalid_moves,
        label="Invalid Moves",
        linewidth=0.5,
    )
    plt.legend()
    plt.xlabel("Number of Trainings")
    plt.ylabel("Number of Invalid Moves Predicted")
    plt.savefig("invalid_goat.png", dpi=300, bbox_inches="tight")
    plt.clf()


def plot_invalid_moves_tiger():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("tiger.csv")

    invalid_moves = data["Predicted Invalid Moves"].apply(
        lambda x: [int(i) for i in eval(x)]
    )
    game_length = data["Turns"].apply(lambda x: [int(i) for i in eval(x)])
    average_invalid_moves = []
    for i in range(len(invalid_moves)):
        average_invalid_moves.append(sum(invalid_moves[i]) / sum(game_length[i]))

    first_quarter = average_invalid_moves[5 : int(len(average_invalid_moves) / 4)]
    print(f"\nMax Average Invalid Moves (Tiger) First Quarter: {max(first_quarter)}")
    print(f"Min Average Invalid Moves (Tiger) First Quarter: {min(first_quarter)}")

    last_half = average_invalid_moves[int(len(average_invalid_moves) / 2) :]
    print(f"Average Invalid Moves (Tiger) Last Half: {sum(last_half)/len(last_half)}")

    print(f"Max Average Invalid Moves (Tiger): {max(average_invalid_moves)}")
    print(f"Min Average Invalid Moves (Tiger): {min(average_invalid_moves)}")

    plt.plot(
        range(len(average_invalid_moves)),
        average_invalid_moves,
        label="Invalid Moves",
        linewidth=0.5,
    )
    plt.legend()
    plt.xlabel("Number of Trainings")
    plt.ylabel("Number of Invalid Moves Predicted")
    plt.savefig("invalid_tiger.png", dpi=300, bbox_inches="tight")
    plt.clf()


def plot_average_turn_goat():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("goat.csv")
    game_length = data["Turns"].apply(lambda x: [int(i) for i in eval(x)])

    half_game = game_length[len(game_length) // 2 :]

    half_avg = [sum(i) / 10 for i in half_game]

    avg_turns = [sum(i) / 10 for i in game_length]

    print(f"\nMax Average Turns Goat: {max(avg_turns)}")
    print(f"Min Average Turns Goat: {min(avg_turns)}")

    avg = sum(half_avg) / len(half_avg)
    print(f"Half game average (Goat): {avg}")

    plt.plot(range(len(avg_turns)), avg_turns, label="Average Turns", linewidth=0.5)
    plt.legend()
    plt.xlabel("Number of Trainings")
    plt.ylabel("Number of Turns")
    plt.savefig("average_turn_goat.png", dpi=300, bbox_inches="tight")
    plt.clf()


def plot_average_turn_tiger():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("tiger.csv")
    game_length = data["Turns"].apply(lambda x: [int(i) for i in eval(x)])

    half_game = game_length[len(game_length) // 2 :]

    half_avg = [sum(i) / 10 for i in half_game]

    avg_turns = [sum(i) / 10 for i in game_length]

    print(f"\nMax Average Turns(Tiger): {max(avg_turns)}")
    print(f"Min Average Turns(Tiger): {min(avg_turns)}")

    avg = sum(half_avg) / len(half_avg)
    print(f"Half game average(Tiger): {avg}")

    plt.plot(range(len(avg_turns)), avg_turns, label="Average Turns", linewidth=0.5)
    plt.legend()
    plt.xlabel("Number of Trainings")
    plt.ylabel("Number of Turns")
    plt.savefig("average_turn_tiger.png", dpi=300, bbox_inches="tight")
    plt.clf()


separate_data("gameplayrecord.csv")
plot_data_tiger()
plot_data_goat()
plot_invalid_moves_goat()
plot_invalid_moves_tiger()
plot_average_turn_goat()
plot_average_turn_tiger()
