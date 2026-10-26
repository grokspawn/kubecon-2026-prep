"""Run validation for the current combined OLM and authored SDK deck."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name("validate-variants.py")), run_name="__main__")
