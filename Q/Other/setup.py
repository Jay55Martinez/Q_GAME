import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "json-stream"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])