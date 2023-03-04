import sys
from os import name

# from .connector import launch_executor


if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)

if sys.argv[1] == "train":
    if len(sys.argv) == 3:
        from .models import models
        from .train import training_loop

        models.load_models(name=sys.argv[2])
        training_loop(model_name=sys.argv[2])
    else:
        from .models import models
        from .train import training_loop

        models.load_models(name=sys.argv[2])

        training_loop()

elif sys.argv[1] == "serve":
    if len(sys.argv) == 3:
        from models import models

        models.load_models(name=sys.argv[2])
        # launch_executor()
    else:
        from models import models

        models.load_models(name=sys.argv[2])
