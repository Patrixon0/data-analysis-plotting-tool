import sys
import os

# Get the absolute path to the submodule
submodule_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "physics-experiment-eval-tool"))

# Add submodule path to sys.path if not already added
if submodule_path not in sys.path:
    sys.path.insert(0, submodule_path)
