import sys
from .connector import launch_executor


if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)

if sys.argv[1] == "train":
    if len(sys.argv) == 3:
        if sys.argv[2] == "clean":
            from .train import training_loop
            training_loop()
    else:
        from .train import training_loop
        from .model import load_model

        load_model()
        training_loop()

elif sys.argv[1] == "serve":
    launch_executor()
