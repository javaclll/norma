import sys
from connector import launch_executor
from gamesimulation import simulate
import os
from constants import MODELPATH 

if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)

if sys.argv[1] == "train":
    if len(sys.argv) == 3:
        if (sys.argv[2] == "clean"):
            simulate()
    else: 
        if not os.path.exists(MODELPATH):
            simulate()

elif sys.argv[1] == "serve":
    launch_executor()
