import sys

# from .connector import launch_executor


if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)

if sys.argv[1] == "train":
    if len(sys.argv) == 3:
        from .train import training_loop
        from .tiger_model import load_model
        from .goat_model import load_model

        load_model(name=sys.argv[2])
        training_loop(model_name=sys.argv[2])
    else:
        from .train import training_loop
        from .tiger_model import load_model
        from .goat_model import load_model

        load_model()
        training_loop()

elif sys.argv[1] == "serve":
    if len(sys.argv) == 3:
        from .tiger_model import load_model
        from .goat_model import load_model

        load_model(name=sys.argv[2])
        # launch_executor()
    else:
        from .tiger_model import load_model
        from .goat_model import load_model

        load_model()
        # launch_executor()
