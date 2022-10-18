import sys
from .connector import launch_executor
from .gamesimulation import simulate
import os
from .constants import GOATMODELPATH, TIGERMODELPATH 
from .agent import Agent
from bagchal import Bagchal

if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)

if sys.argv[1] == "train":
    if len(sys.argv) == 3:
        if (sys.argv[2] == "clean"):
            simulate()
    else: 
        if not os.path.exists(GOATMODELPATH) or not os.path.exists(TIGERMODELPATH):
            simulate()

elif sys.argv[1] == "serve":
    launch_executor()

elif sys.argv[1] == "test":
    agentOne = Agent(1)
    game = Bagchal.new()

    agentOne.moveState(game)