import csv
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
    plt.title("Tiger Wins, Loss and Draws Over Time")
    plt.legend()

    plt.savefig("tiger.png", dpi=300, bbox_inches="tight")


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

    plt.title("Goat Wins, Loss and Draws Over Time")
    plt.legend()

    plt.xlabel("Number of Traninigs")
    plt.ylabel("Number of Games")

    plt.savefig("goat.png", dpi=300, bbox_inches="tight")


separate_data("gameplayrecord.csv")
plot_data_tiger()
plt.clf()
plot_data_goat()
