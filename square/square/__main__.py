import sys
from .connector import launch_executor


if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)


if sys.argv[1] == "serve":
    launch_executor()
