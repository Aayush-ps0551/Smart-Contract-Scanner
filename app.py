import streamlit as st
import tempfile
import os
from core.slither_runner import run_slither

# Set up the page configuration and theme
st.set_page_config(page_title="Web3 Vulnerability Scanner", page_icon="🛡️", layout="wide")

# --- SPACE THEME CSS ---
st.markdown(
    """
    <style>
    /* Shooting stars background GIF */
    .stApp {
        background-image: url("https://media.giphy.com/media/aBovVqWw0J3aI/giphy.gif");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Transparent dark overlay for main content readability */
    .block-container {
        background-color: rgba(10, 10, 25, 0.85);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0px 0px 20px rgba(0, 191, 255, 0.4);
        border: 1px solid rgba(0, 191, 255, 0.3);
    }

    /* Cosmic Blue titles */
    h1, h2, h3 {
        color: #00BFFF !important;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 0px 0px 10px rgba(0, 191, 255, 0.8);
    }
    
    /* Transparent Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 25, 0.85) !important;
        border-right: 1px solid rgba(0, 191, 255, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

st.markdown("### Choose a Contract to Scan")
input_method = st.radio("Select Input Method:", ["Upload your own file", "Try a sample dataset"], horizontal=True)

file_content = None
file_name = None

if input_method == "Upload your own file":
    uploaded_file = st.file_uploader("Upload a Solidity File", type=["sol"])
    if uploaded_file is not None:
        file_content = uploaded_file.getvalue()
        file_name = uploaded_file.name
else:
    contracts_dir = "contracts"
    if os.path.exists(contracts_dir):
        sample_files = [f for f in os.listdir(contracts_dir) if f.endswith(".sol")]
        if sample_files:
            selected_sample = st.selectbox("Select a pre-existing vulnerable contract:", sample_files)
            if selected_sample:
                with open(os.path.join(contracts_dir, selected_sample), "r", encoding="utf-8") as f:
                    file_content = f.read().encode("utf-8")
                file_name = selected_sample
        else:
            st.warning("No sample files found in the 'contracts' folder.")
    else:
        st.warning("The 'contracts' folder does not exist.")

if file_content is not None and file_name is not None:
    # Save the file to a temporary location so Slither can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".sol") as tmp_file:
        tmp_file.write(file_content)
        tmp_file_path = tmp_file.name

    # Create interactive layout tabs
    tab1, tab2 = st.tabs(["🔍 Scan Center", "📜 Source Code"])
    
    with tab2:
        st.markdown("### Contract Source Code")
        st.code(file_content.decode("utf-8"), language="solidity")

    with tab1:
        st.info(f"Ready to scan **{file_name}**")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            scan_btn = st.button("🚀 Run Security Scan", type="primary", use_container_width=True)
            
        if scan_btn:
            with st.spinner("Analyzing smart contract with Slither... Please wait."):
                success, output = run_slither(tmp_file_path)
                
                st.markdown("---")
                if success and isinstance(output, dict):
                    if output.get('success'):
                        detectors = output.get('results', {}).get('detectors', [])
                        
                        if not detectors:
                            st.success("✅ **Scan Passed!** No vulnerabilities found by Slither.")
                        else:
                            st.error(f"⚠️ **Vulnerabilities Detected!** Found {len(detectors)} issues.")
                            
                            st.markdown("### 📊 Vulnerability Summary")
                            
                            # Count severities
                            high = sum(1 for d in detectors if d.get('impact') == 'High')
                            medium = sum(1 for d in detectors if d.get('impact') == 'Medium')
                            low = sum(1 for d in detectors if d.get('impact') == 'Low')
                            info = sum(1 for d in detectors if d.get('impact') == 'Informational')
                            
                            c1, c2, c3, c4 = st.columns(4)
                            c1.metric("🔴 High Severity", high)
                            c2.metric("🟠 Medium Severity", medium)
                            c3.metric("🟡 Low Severity", low)
                            c4.metric("🔵 Informational", info)
                            
                            st.markdown("### 📋 Detailed Findings")
                            for idx, d in enumerate(detectors):
                                impact = d.get('impact', 'Unknown')
                                check_name = d.get('check', 'Unknown Check')
                                
                                # Emoji based on severity
                                emoji = "🔴" if impact == "High" else "🟠" if impact == "Medium" else "🟡" if impact == "Low" else "🔵"
                                
                                with st.expander(f"{emoji} [{impact}] {check_name}"):
                                    st.markdown(d.get('markdown', d.get('description', 'No description available.')))
                                    st.caption(f"**Confidence:** {d.get('confidence', 'N/A')}")
                                    if 'reference' in d:
                                        st.markdown(f"[Learn more about this vulnerability]({d['reference']})")
                    else:
                        st.error("❌ Slither returned an error state.")
                        st.text(output.get('error', 'Unknown Error'))

                else:
                    st.error("❌ Error running scan (Compilation failed). Please check your Solidity syntax.")
                    with st.expander("Error Details", expanded=True):
                        st.text_area("Logs", output, height=300)
