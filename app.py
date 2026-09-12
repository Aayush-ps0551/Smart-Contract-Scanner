import streamlit as st
import tempfile
import os
from core.slither_runner import run_slither

# Set up the page configuration and theme
st.set_page_config(page_title="Web3 Vulnerability Scanner", page_icon="🛡️", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Scanner Settings")
    st.markdown("Configure the vulnerability scanning engines.")
    
    st.markdown("### Active Engines")
    use_slither = st.checkbox("Slither (Static Analysis)", value=True, disabled=True)
    use_mythril = st.checkbox("Mythril (Symbolic Execution)", value=False, disabled=True, help="Coming soon!")
    use_echidna = st.checkbox("Echidna (Fuzzing)", value=False, disabled=True, help="Coming soon!")
    
    st.markdown("---")
    st.markdown("### About")
    st.info("An automated Web3 security tool to find vulnerabilities in Solidity smart contracts before deployment. It wraps powerful command-line tools into an easy-to-use interface.")

# --- MAIN UI ---
st.title("🛡️ Web3 Smart Contract Vulnerability Scanner")
st.markdown("Upload your Solidity (`.sol`) file to instantly detect vulnerabilities such as **Re-entrancy**, **Integer Overflow**, and **Access Control** issues.")

# File Uploader
uploaded_file = st.file_uploader("Upload a Solidity File", type=["sol"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location so Slither can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".sol") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Create interactive layout tabs
    tab1, tab2 = st.tabs(["🔍 Scan Center", "📜 Source Code"])
    
    with tab2:
        st.markdown("### Contract Source Code")
        st.code(uploaded_file.getvalue().decode("utf-8"), language="solidity")

    with tab1:
        st.info(f"Ready to scan **{uploaded_file.name}**")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            scan_btn = st.button("🚀 Run Security Scan", type="primary", use_container_width=True)
            
        if scan_btn:
            with st.spinner("Analyzing smart contract with Slither... Please wait."):
                success, output = run_slither(tmp_file_path)
                
                st.markdown("---")
                if success:
                    # Simple heuristic to check if Slither found issues 
                    # (Slither usually outputs "Reference: https..." when it finds vulnerabilities)
                    if "Reference:" in output or "issues" in output.lower() or "Reentrancy" in output:
                        st.error("⚠️ **Vulnerabilities Detected!** Please review the report below.")
                    else:
                        st.success("✅ **Scan Passed!** No major vulnerabilities found by Slither.")
                        
                    st.markdown("### Detailed Scan Report")
                    
                    # Use an expander to keep the UI clean
                    with st.expander("View Raw Slither Output", expanded=True):
                        st.text(output)
                else:
                    st.error("❌ Error running scan. Make sure Slither and solc are installed.")
                    with st.expander("Error Details", expanded=True):
                        st.text_area("Logs", output, height=200)
