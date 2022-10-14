import sys
from .connector import launch_executor
from .model import load_model


if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)

if sys.argv[1] == "train":
    if len(sys.argv == 2) and (sys.argv[2] == "clean"):
        pass
    else:
        load_model()

elif sys.argv[1] == "serve":
    launch_executor()
