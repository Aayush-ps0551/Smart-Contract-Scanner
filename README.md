# 🛡️ Web3 Smart Contract Vulnerability Scanner

**🚀 Live Demo:** *[Link to be added]*

An automated, interactive UI wrapper for industry-standard smart contract security tools (like Slither). This tool helps Web3 developers find flaws in their Solidity code (e.g., Re-entrancy, Integer Overflow, Access Control) before deployment.

## 🏗 Architecture & Folder Structure

The project is designed to be highly modular and easy to understand so you can expand it with more tools:

```text
Web3Scanner/
│
├── app.py                  # The main Streamlit frontend (UI logic)
├── run.py                  # Helper script to launch the app easily using python
├── start.bat               # Windows batch file to double-click and run the app
├── requirements.txt        # Python dependencies
│
├── core/                   # The backend engine
│   ├── __init__.py
│   └── slither_runner.py   # Wrapper that executes Slither CLI and captures output
│
└── contracts/              # Sample Solidity contracts for testing
    └── Vulnerable.sol      # Example contract with a Re-entrancy bug
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Web3Scanner.git
cd Web3Scanner
```

### 2. Set up the Python environment
Create a virtual environment and install the dependencies:
```bash
# Create Virtual Environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate
# Activate it (Mac/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Install the Solidity Compiler (solc)
Slither requires `solc` to compile and analyze the contracts:
```bash
solc-select install 0.8.0
solc-select use 0.8.0
```

### 4. Run the Application
You can easily start the application using the provided helper scripts:
- **Windows:** Double-click `start.bat`
- **Any OS:** Run `python run.py`

Alternatively, you can run the Streamlit command directly:
```bash
streamlit run app.py
```

## 🔮 Future Roadmap
- [ ] Parse Slither JSON output for advanced vulnerability dashboards.
- [ ] Integrate **Mythril** for deep symbolic execution.
- [ ] Integrate **Echidna** for fuzzing tests.
