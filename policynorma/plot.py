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

    new_data = data[::5]

    wins = new_data["Wins"]
    loss = new_data["Loss"]
    # draw = new_data["Draw"]
    time = np.arange(len(new_data)) * 5

    plt.plot(time, wins, label="Wins", linewidth=0.5)
    plt.plot(time, loss, label="Loss" ,linewidth=0.5)
    # plt.plot(time, draw, label="Draw")

    plt.xlabel("Number of Trainings")
    plt.ylabel("Number of Games")
    plt.title("Tiger Wins, Loss Over Time")
    plt.legend()

    plt.savefig("tiger.png", dpi=300, bbox_inches="tight")
    plt.clf()


def plot_data_goat():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("goat.csv")
    data.pop("Predicted Invalid Moves")
    data.pop("Turns")
    new_data = data.rolling(8).min().iloc[::8]

    wins = new_data["Wins"]
    loss = new_data["Loss"]
    draw = new_data["Draw"]
    time = np.arange(len(new_data)) * 8

    plt.plot(time, wins, label="Wins",linewidth=0.5)
    plt.plot(time, loss, label="Loss",linewidth=0.5)
    plt.plot(time, draw, label="Draw",linewidth=0.5)

    plt.title("Goat Wins, Loss and Draws Over Time")
    plt.legend()

    plt.xlabel("Number of Trainings")
    plt.ylabel("Number of Games")

    plt.savefig("goat.png", dpi=300, bbox_inches="tight")
    plt.clf()

def plot_invalid_moves_goat():
    print("Printing goat")
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("goat.csv")

    invalid_moves = data["Predicted Invalid Moves"].apply(
        lambda x: [int(i) for i in eval(x)]
    )
    game_length = data["Turns"].apply(lambda x: [int(i) for i in eval(x)])
    average_invalid_moves = []
    for i in range(len(invalid_moves)):
        average_invalid_moves.append(sum(invalid_moves[i])/sum(game_length[i]))

    plt.plot(range(len(average_invalid_moves)), average_invalid_moves, label="Invalid Moves",linewidth=0.5)
    plt.title("No of invalid moves predicted over time (Goat)")
    plt.legend()
    plt.xlabel("Number of Trainings")
    plt.ylabel("Number of Invalid Moves Predicted")
    plt.savefig("invalid_goat.png", dpi=300, bbox_inches="tight")
    plt.clf()

def plot_invalid_moves_tiger():
    print("Printing goat")
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("tiger.csv")

    invalid_moves = data["Predicted Invalid Moves"].apply(
        lambda x: [int(i) for i in eval(x)]
    )
    game_length = data["Turns"].apply(lambda x: [int(i) for i in eval(x)])
    average_invalid_moves = []
    for i in range(len(invalid_moves)):
        average_invalid_moves.append(sum(invalid_moves[i])/sum(game_length[i]))

    plt.plot(range(len(average_invalid_moves)), average_invalid_moves, label="Invalid Moves",linewidth=0.5)
    plt.title("No of invalid moves predicted over time (Tiger)")
    plt.legend()
    plt.xlabel("Number of Trainings")
    plt.ylabel("Number of Invalid Moves Predicted")
    plt.savefig("invalid_tiger.png", dpi=300, bbox_inches="tight")
    plt.clf()

separate_data("gameplayrecord.csv")
plot_data_tiger()
plot_data_goat()
plot_invalid_moves_goat()
plot_invalid_moves_tiger()

