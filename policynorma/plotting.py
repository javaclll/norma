import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


# def separate_data(file):
#     with open(file, "r") as data:
#         reader = csv.reader(data)

#         with open("agentplayrecord.csv", "w") as agent:
#             agent_writer = csv.writer(agent)

#             agent_writer.writerow(
#                 [
#                     "Norma Agent",
#                     "Wins",
#                     "Loss",
#                     "Draw",
#                     "Game No",
#                     "Predicted Invalid Moves",
#                     "Turns",
#                 ]
#             )

#             for row in reader:
#                 if row[0] == "1":
#                     agent_writer.writerow(row)


def plot_data():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    data = pd.read_csv("agentplayrecord.csv")

    wins = data["Wins"][::2]
    loss = data["Loss"][::2]
    draw = data["Draw"][::2]
    print(wins.shape)
    print(loss.shape)
    print(draw.shape)
    x_axis = ["Tiger Wins", "Draw", "Goat Wins"]
    print(data["Wins"][81])
    y_axis = [
        data["Loss"][81],
        data["Draw"][81],
        data["Wins"][81],
    ]
    time = np.arange(-1, len(data) / 2)
    print(len(time))
    colors = ["grey", "grey", "grey"]
    plt.bar(x_axis, y_axis, color=colors)

    plt.ylabel("No of Games")
    plt.title("Tiger Agent vs Goat Agent over 2001 Games")

    plt.savefig("agentplay.png", dpi=300, bbox_inches="tight")


plot_data()
