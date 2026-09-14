import subprocess
import os
import json
import tempfile
import re

def get_solidity_version(file_path):
    """
    Parses the .sol file to find the pragma solidity version.
    Returns the version string or '0.8.0' as fallback.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Match formats like: pragma solidity ^0.8.19; or >=0.8.0 <0.9.0;
            match = re.search(r'pragma solidity\s+[^0-9]*([0-9]+\.[0-9]+\.[0-9]+)', content)
            if match:
                return match.group(1)
    except Exception:
        pass
    return "0.8.0" # Default fallback

def run_slither(file_path):
    """
    Runs Slither on the given Solidity file.
    Returns (success_boolean, output_data)
    """
    try:
        # 1. Auto-detect the required Solidity version
        version = get_solidity_version(file_path)
        
        # 2. Ensure that specific solc version is installed and active
        subprocess.run(["solc-select", "install", version], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["solc-select", "use", version], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 3. Get a temporary file path for JSON output, but don't create it yet
        # (Slither refuses to overwrite an existing JSON file)
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            json_out_path = f.name
        os.remove(json_out_path)
            
        # 4. Run Slither
        result = subprocess.run(
            ["slither", file_path, "--json", json_out_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 5. Check if JSON file was successfully created
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
        return False, "Slither or solc-select is not installed or not in the PATH."
    except Exception as e:
        return False, str(e)
