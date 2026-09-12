import subprocess
import os

def run_slither(file_path):
    """
    Runs Slither on the given Solidity file.
    Returns (success_boolean, output_string)
    """
    try:
        # Running slither and capturing the standard text output
        result = subprocess.run(
            ["slither", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Combine stdout and stderr since slither prints warnings/results to stderr sometimes
        output = result.stdout + "\n" + result.stderr
        
        return True, output

    except FileNotFoundError:
        return False, "Slither is not installed or not in the PATH."
    except Exception as e:
        return False, str(e)
