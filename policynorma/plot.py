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

    win_percent_max = max(data["Wins"])
    win_percent_min = min(data["Wins"])
    print(f"Max Win Tiger: {win_percent_max * 5}")
    print(f"Min Win Tiger: {win_percent_min *5}")

    loss_percent_max = max(data["Loss"])
    loss_percent_min = min(data["Loss"])
    print(f"Max Loss Tiger: {loss_percent_max * 5}")
    print(f"Min Loss Tiger: {loss_percent_min * 5}")
    print()

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
    plt.legend()

    plt.savefig("tiger.png", dpi=300, bbox_inches="tight")
    plt.clf()


def plot_data_goat():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("goat.csv")
    data.pop("Predicted Invalid Moves")
    data.pop("Turns")

    win_percent_max = max(data["Wins"])
    win_percent_min = min(data["Wins"])
    print(f"Max Win Goat: {win_percent_max * 5}")
    print(f"Min Win Goat: {win_percent_min *5}")

    loss_percent_max = max(data["Loss"])
    loss_percent_min = min(data["Loss"])
    print(f"Max Loss Goat: {loss_percent_max * 5}")
    print(f"Min Loss Goat: {loss_percent_min * 5}")

    draw_percent_max = max(data["Draw"])
    draw_percent_min = min(data["Draw"])
    print(f"Max Draw Goat: {draw_percent_max * 5}")
    print(f"Min Draw Goat: {draw_percent_min * 5}")

    wins = data["Wins"].rolling(8).max().iloc[::8]

    loss = data["Loss"].rolling(8).min().iloc[::8]

    draw = data["Draw"].rolling(8).max().iloc[::8]

    time = np.arange(len(data[::8]))

    plt.plot(time, wins, label="Wins",linewidth=0.5)
    plt.plot(time, loss, label="Loss",linewidth=0.5)
    plt.plot(time, draw, label="Draw",linewidth=0.5)

    plt.legend()

    plt.xlabel("Number of Trainings")
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
        average_invalid_moves.append(sum(invalid_moves[i])/sum(game_length[i]))

    print(f"\nMax Average Invalid Moves (Goat): {max(average_invalid_moves)}")
    print(f"Min Average Invalid Moves (Goat): {min(average_invalid_moves)}")

    plt.plot(range(len(average_invalid_moves)), average_invalid_moves, label="Invalid Moves",linewidth=0.5)
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
        average_invalid_moves.append(sum(invalid_moves[i])/sum(game_length[i]))
    
    first_quarter = average_invalid_moves[5:int(len(average_invalid_moves)/4)]
    print(f"\nMax Average Invalid Moves (Tiger) First Quarter: {max(first_quarter)}")
    print(f"Min Average Invalid Moves (Tiger) First Quarter: {min(first_quarter)}")

    last_half = average_invalid_moves[int(len(average_invalid_moves)/2):]
    print(f"Average Invalid Moves (Tiger) Last Half: {sum(last_half)/len(last_half)}")
    
    print(f"Max Average Invalid Moves (Tiger): {max(average_invalid_moves)}")
    print(f"Min Average Invalid Moves (Tiger): {min(average_invalid_moves)}")

    plt.plot(range(len(average_invalid_moves)), average_invalid_moves, label="Invalid Moves",linewidth=0.5)
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

    half_game = game_length[len(game_length)//2:]
    
    half_avg = [sum(i)/10 for i in half_game]

    avg_turns = [sum(i)/10 for i in game_length]

    print(f"\nMax Average Turns Goat: {max(avg_turns)}")
    print(f"Min Average Turns Goat: {min(avg_turns)}")

    avg = sum(half_avg)/len(half_avg)
    print(f"Half game average (Goat): {avg}")

    plt.plot(range(len(avg_turns)),avg_turns, label="Average Turns",linewidth=0.5)
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

    half_game = game_length[len(game_length)//2:]
    
    half_avg = [sum(i)/10 for i in half_game]

    avg_turns = [sum(i)/10 for i in game_length]

    print(f"\nMax Average Turns(Tiger): {max(avg_turns)}")
    print(f"Min Average Turns(Tiger): {min(avg_turns)}")

    avg = sum(half_avg)/len(half_avg)
    print(f"Half game average(Tiger): {avg}")
 
    plt.plot(range(len(avg_turns)),avg_turns, label="Average Turns",linewidth=0.5)
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

