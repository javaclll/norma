import sys
from .connector import launch_executor
from .gamesimulation import Simulator
import os
from .constants import GOATMODELPATH, TARGETMODELPATH, TIGERMODELPATH 
from bagchal import Bagchal

if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)

if sys.argv[1] == "train":
    if len(sys.argv) == 3:
        if (sys.argv[2] == "clean"):
            simulator = Simulator()
            simulator.simulate()
    else: 
        if not os.path.exists(GOATMODELPATH) or not os.path.exists(TARGETMODELPATH):
            simulator = Simulator()
            simulator.simulate()

elif sys.argv[1] == "serve":
    launch_executor()
