import sys
import absl.logging
from .connector import launch_executor
from .datageneration import Generator

absl.logging.set_verbosity(absl.logging.ERROR)

if len(sys.argv) == 1:
    print("Missing arguments!")
    print("Please use `train` or `serve` !")
    exit(0)

if sys.argv[1] == "train":
    generator = Generator()
    generator.generate()


elif sys.argv[1] == "serve":
    launch_executor()
