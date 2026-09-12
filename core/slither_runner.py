import subprocess
import os
import json
import tempfile

def run_slither(file_path):
    """
    Runs Slither on the given Solidity file.
    Returns (success_boolean, output_data)
    output_data is a dictionary if JSON parsing succeeds, else a string.
    """
    try:
        # Create a temporary file for JSON output
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            json_out_path = f.name
            
        result = subprocess.run(
            ["slither", file_path, "--json", json_out_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Check if JSON file was successfully created and populated
        if os.path.exists(json_out_path) and os.path.getsize(json_out_path) > 0:
            with open(json_out_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            os.remove(json_out_path)
            return True, data
        else:
            # Fallback if JSON wasn't created (e.g. syntax error in .sol)
            output = result.stdout + "\n" + result.stderr
            if os.path.exists(json_out_path):
                os.remove(json_out_path)
            return False, output

    except FileNotFoundError:
        return False, "Slither is not installed or not in the PATH."
    except Exception as e:
        return False, str(e)
