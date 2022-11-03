import sys
from .connector import launch_executor


if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)

if sys.argv[1] == "train":
    if len(sys.argv) == 3:
        if sys.argv[2] == "clean":
            print("Clean train disabled. Delete model and run to clean train!")
            # from .train import training_loop
            # training_loop()
    else:
        from .train import training_loop
        from .model import load_model

        load_model()
        training_loop()

elif sys.argv[1] == "serve":
    from .model import load_model
    load_model()
    launch_executor()

elif sys.argv[1] == "test":
    from .train import test
    test()
