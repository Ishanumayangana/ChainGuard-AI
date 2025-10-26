import streamlit as st
import json
import time
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from blockchain import Blockchain, SecurityModule
from ai_module import AIModule

# Page configuration
st.set_page_config(
    page_title="Blockchain + AI + Security Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    .main {
        background: transparent;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(103, 126, 234, 0.8);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #b8b8d4 !important;
        font-size: 14px;
        font-weight: 500;
    }
    
    div[data-testid="stMetricDelta"] {
        color: #4ade80 !important;
    }
    
    /* Card Containers */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 15px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 10px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #b8b8d4;
        font-weight: 600;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Block Cards */
    .block-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    
    .block-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Error/Info Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Code Blocks */
    .stCodeBlock {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Radio Buttons */
    .stRadio > label {
        color: #b8b8d4 !important;
        font-weight: 500;
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Animations */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Glass Morphism Effect */
    .glass {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain(difficulty=4)
    st.session_state.ai_module = AIModule()
    st.session_state.security = SecurityModule()
    st.session_state.ai_module.train_anomaly_detector(st.session_state.blockchain.get_chain())
    st.session_state.rsa_encrypted = None
    st.session_state.aes_data = {}
    st.session_state.signature = None
    st.session_state.notifications = []

blockchain = st.session_state.blockchain
ai_module = st.session_state.ai_module
security = st.session_state.security

# Helper function for notifications
def show_notification(message, type="info"):
    if type == "success":
        st.success(f"✅ {message}")
    elif type == "error":
        st.error(f"❌ {message}")
    elif type == "warning":
        st.warning(f"⚠️ {message}")
    else:
        st.info(f"ℹ️ {message}")

# Title with animated header
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🔐 Blockchain + AI + Security</h1>
    <p style='font-size: 1.3rem; color: #b8b8d4; margin-top: 0.5rem;'>
        Advanced Distributed Ledger Technology with AI-Powered Analytics & Military-Grade Cryptography
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced metrics
with st.sidebar:
    st.markdown("### 📊 Live System Metrics")
    
    stats = blockchain.get_chain_stats()
    chain = blockchain.get_chain()
    health = ai_module.get_blockchain_health_score(chain, stats['is_valid'])
    
    # Create metrics with better styling
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔗 Blocks", stats['total_blocks'], delta="Active")
    with col2:
        st.metric("⚡ Difficulty", stats['difficulty'], delta="Mining")
    
    # Health score with color coding
    health_score = health['health_score']
    if health_score >= 80:
        st.metric("❤️ Health", f"{health_score}%", delta="Excellent", delta_color="normal")
    elif health_score >= 60:
        st.metric("💛 Health", f"{health_score}%", delta="Good", delta_color="normal")
    else:
        st.metric("🔴 Health", f"{health_score}%", delta="Check", delta_color="inverse")
    
    # Chain validity indicator
    if stats['is_valid']:
        st.success("✅ Chain Valid")
    else:
        st.error("❌ Chain Invalid")
    
    st.divider()
    
    # Navigation with icons
    st.markdown("### 🧭 Navigation Panel")
    page = st.radio(
        "",
        ["🏠 Dashboard", "⛓️ Blockchain", "🔐 Security Suite", "🤖 AI Analytics", "📈 Visualizations"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Real-time stats
    st.markdown("### ⏱️ Real-Time Stats")
    analysis = ai_module.analyze_blockchain_patterns(chain)
    if 'total_blocks' in analysis and analysis['total_blocks'] > 1:
        st.metric("📊 Avg Nonce", f"{analysis['average_nonce']:.0f}")
        st.metric("⏱️ Avg Time", f"{analysis['avg_block_time']:.2f}s")
        st.caption(f"Trend: {analysis['mining_difficulty_trend']}")


# Main content based on page selection
if page == "🏠 Dashboard":
    st.markdown("## 🏠 System Dashboard")
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Blocks", stats['total_blocks'], delta=f"+{stats['total_blocks']-1} mined")
    with col2:
        st.metric("Mining Difficulty", stats['difficulty'], delta="Proof of Work")
    with col3:
        chain_status = "SECURE" if stats['is_valid'] else "COMPROMISED"
        st.metric("Chain Status", chain_status, delta="Verified")
    with col4:
        st.metric("Health Score", f"{health['health_score']}%", delta="AI Analyzed")
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Block Mining Trends")
        if len(chain) > 1:
            # Create nonce trend chart
            block_indices = [b['index'] for b in chain]
            nonces = [b['nonce'] for b in chain]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=block_indices,
                y=nonces,
                mode='lines+markers',
                name='Nonce',
                line=dict(color='#667eea', width=3),
                marker=dict(size=10, color='#764ba2')
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.05)',
                font=dict(color='white'),
                xaxis_title="Block Index",
                yaxis_title="Nonce Value",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add more blocks to see mining trends")
    
    with col2:
        st.markdown("#### 🎯 System Health Breakdown")
        health_metrics = health.get('metrics', {})
        
        if health_metrics:
            categories = ['Chain Valid', 'Block Count', 'AI Status']
            values = [
                100 if stats['is_valid'] else 0,
                min(stats['total_blocks'] * 10, 100),
                health_score
            ]
            
            fig = go.Figure(data=[go.Bar(
                x=categories,
                y=values,
                marker=dict(color=['#10b981', '#667eea', '#764ba2']),
                text=[f"{v}%" for v in values],
                textposition='auto'
            )])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.05)',
                font=dict(color='white'),
                yaxis=dict(range=[0, 100]),
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Recent blocks section
    st.markdown("#### 🔗 Recent Blocks")
    
    if len(chain) > 1:
        recent_blocks = chain[-5:][::-1]  # Last 5 blocks, reversed
        
        for block in recent_blocks:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
                
                with col1:
                    if block['index'] == 0:
                        st.markdown("🌟 **Genesis**")
                    else:
                        st.markdown(f"**Block #{block['index']}**")
                
                with col2:
                    st.markdown(f"`{block['hash'][:20]}...`")
                
                with col3:
                    st.markdown(f"Nonce: **{block['nonce']}**")
                
                with col4:
                    timestamp = datetime.fromtimestamp(block['timestamp'])
                    st.markdown(f"🕐 {timestamp.strftime('%H:%M:%S')}")
                
                with col5:
                    # Check if block is anomaly
                    anomaly = ai_module.detect_anomaly(block)
                    if anomaly.get('is_anomaly'):
                        st.markdown("⚠️ Anomaly")
                    else:
                        st.markdown("✅ Normal")
                
                st.divider()
    else:
        st.info("Add blocks to see them here")
    
    # Quick actions
    st.markdown("#### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⛏️ Mine New Block", use_container_width=True):
            st.session_state.quick_action = "mine"
            st.rerun()
    
    with col2:
        if st.button("🔐 Encrypt Data", use_container_width=True):
            st.session_state.quick_action = "encrypt"
            st.rerun()
    
    with col3:
        if st.button("🤖 Run AI Analysis", use_container_width=True):
            st.session_state.quick_action = "ai"
            st.rerun()
    
    with col4:
        if st.button("✅ Validate Chain", use_container_width=True):
            with st.spinner("Validating blockchain..."):
                is_valid = blockchain.is_chain_valid()
            if is_valid:
                st.success("✅ Blockchain is valid!")
            else:
                st.error("❌ Blockchain validation failed!")

elif page == "⛓️ Blockchain":
    st.header("⛓️ Blockchain Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Add New Block")
        
        # Transaction input
        transaction_data = st.text_area(
            "Transaction Data (JSON format):",
            value='{"sender": "Alice", "receiver": "Bob", "amount": 100}',
            height=100
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("⛏️ Add Block & Mine", type="primary"):
                try:
                    data = json.loads(transaction_data)
                    with st.spinner("Mining block... Please wait"):
                        new_block = blockchain.add_block(data)
                        ai_module.train_anomaly_detector(blockchain.get_chain())
                        anomaly_result = ai_module.detect_anomaly(new_block.to_dict())
                    
                    st.success(f"✅ Block #{new_block.index} mined successfully!")
                    st.info(f"**Hash:** `{new_block.hash[:20]}...`")
                    st.info(f"**Nonce:** {new_block.nonce}")
                    
                    if anomaly_result.get('is_anomaly'):
                        st.warning("⚠️ Anomaly detected in new block!")
                    
                    st.rerun()
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with col_btn2:
            if st.button("🔄 Refresh Chain"):
                st.rerun()
        
        with col_btn3:
            if st.button("✅ Validate Chain"):
                is_valid = blockchain.is_chain_valid()
                if is_valid:
                    st.success("✅ Blockchain is valid!")
                else:
                    st.error("❌ Blockchain validation failed!")
    
    with col2:
        st.subheader("📈 Statistics")
        analysis = ai_module.analyze_blockchain_patterns(blockchain.get_chain())
        
        if 'total_blocks' in analysis:
            st.metric("Avg Nonce", f"{analysis['average_nonce']:.0f}")
            st.metric("Max Nonce", analysis['max_nonce'])
            st.metric("Avg Block Time", f"{analysis['avg_block_time']:.2f}s")
            st.info(f"**Mining Trend:** {analysis['mining_difficulty_trend']}")
    
    # Blockchain Visualization
    st.divider()
    st.subheader("📊 Blockchain Visualization")
    
    chain = blockchain.get_chain()
    
    for block in chain:
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"**Block #{block['index']}**")
            with col2:
                st.markdown(f"**Hash:** `{block['hash'][:16]}...`")
            with col3:
                st.markdown(f"**Nonce:** {block['nonce']}")
            with col4:
                st.markdown(f"**Time:** {time.strftime('%H:%M:%S', time.localtime(block['timestamp']))}")
            
            st.divider()

elif page == "Security Tools":
    st.header("🔐 Security & Cryptography Tools")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔢 Hashing", "🔒 RSA Encryption", "🔐 AES Encryption", "✍️ Digital Signatures"])
    
    with tab1:
        st.subheader("Hashing Module")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            hash_input = st.text_input("Data to Hash:", value="Hello Blockchain")
        with col2:
            hash_algo = st.selectbox("Algorithm:", ["sha256", "sha512", "md5"])
        
        if st.button("Generate Hash", key="hash_btn"):
            hashed = security.hash_data(hash_input, hash_algo)
            st.success("Hash generated successfully!")
            st.code(hashed, language="text")
            st.info(f"**Algorithm:** {hash_algo.upper()}")
    
    with tab2:
        st.subheader("RSA Encryption/Decryption (2048-bit)")
        
        rsa_input = st.text_input("Data to Encrypt/Decrypt:", value="Secret Message", key="rsa_input")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔒 Encrypt (RSA)", type="primary"):
                encrypted = security.rsa_encrypt(rsa_input)
                st.session_state.rsa_encrypted = encrypted
                st.success("Encrypted successfully!")
                st.code(encrypted[:100] + "...", language="text")
        
        with col2:
            if st.button("🔓 Decrypt (RSA)"):
                if st.session_state.rsa_encrypted:
                    decrypted = security.rsa_decrypt(st.session_state.rsa_encrypted)
                    st.success("Decrypted successfully!")
                    st.code(decrypted, language="text")
                else:
                    st.warning("Please encrypt data first!")
    
    with tab3:
        st.subheader("AES Encryption/Decryption (256-bit CBC)")
        
        aes_input = st.text_input("Data to Encrypt/Decrypt:", value="Confidential Data", key="aes_input")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔒 Encrypt (AES)", type="primary"):
                result = security.aes_encrypt(aes_input)
                st.session_state.aes_data = result
                st.success("Encrypted successfully!")
                st.code(result['ciphertext'][:80] + "...", language="text")
                with st.expander("View Key & IV"):
                    st.text(f"Key: {result['key'][:40]}...")
                    st.text(f"IV: {result['iv']}")
        
        with col2:
            if st.button("🔓 Decrypt (AES)"):
                if st.session_state.aes_data:
                    decrypted = security.aes_decrypt(
                        st.session_state.aes_data['ciphertext'],
                        st.session_state.aes_data['key'],
                        st.session_state.aes_data['iv']
                    )
                    st.success("Decrypted successfully!")
                    st.code(decrypted, language="text")
                else:
                    st.warning("Please encrypt data first!")
    
    with tab4:
        st.subheader("Digital Signatures (ECDSA - Secp256k1)")
        
        sign_input = st.text_input("Data to Sign:", value="Important Document", key="sign_input")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✍️ Sign Data", type="primary"):
                signature = security.sign_data(sign_input)
                st.session_state.signature = signature
                st.success("Data signed successfully!")
                st.code(signature, language="text")
        
        with col2:
            if st.button("✅ Verify Signature"):
                if st.session_state.signature:
                    is_valid = security.verify_signature(sign_input, st.session_state.signature)
                    if is_valid:
                        st.success("✅ Signature is VALID!")
                    else:
                        st.error("❌ Signature is INVALID!")
                else:
                    st.warning("Please sign data first!")

else:  # AI Analytics
    st.header("🤖 AI/ML Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📊 Blockchain Analysis", "⚠️ Risk Assessment", "🔍 Anomaly Detection"])
    
    with tab1:
        st.subheader("Blockchain Pattern Analysis")
        
        if st.button("🔍 Analyze Blockchain", type="primary"):
            with st.spinner("Analyzing blockchain patterns..."):
                analysis = ai_module.analyze_blockchain_patterns(blockchain.get_chain())
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Blocks", analysis.get('total_blocks', 0))
                st.metric("Average Nonce", f"{analysis.get('average_nonce', 0):.2f}")
            
            with col2:
                st.metric("Max Nonce", analysis.get('max_nonce', 0))
                st.metric("Min Nonce", analysis.get('min_nonce', 0))
            
            with col3:
                st.metric("Avg Block Time", f"{analysis.get('avg_block_time', 0):.2f}s")
                st.info(f"**Trend:** {analysis.get('mining_difficulty_trend', 'N/A')}")
        
        if st.button("🧠 Train AI Model"):
            with st.spinner("Training AI model..."):
                result = ai_module.train_anomaly_detector(blockchain.get_chain())
            
            if result['status'] == 'success':
                st.success(f"✅ Model trained with {result['samples_trained']} samples!")
            else:
                st.error(f"❌ Training failed: {result['message']}")
    
    with tab2:
        st.subheader("Transaction Risk Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            risk_amount = st.number_input("Transaction Amount:", min_value=0, value=5000, step=100)
        
        with col2:
            risk_data = st.text_input("Transaction Data:", value="Large transfer")
        
        if st.button("🎯 Assess Risk", type="primary"):
            result = ai_module.predict_transaction_risk({
                'amount': risk_amount,
                'data': risk_data,
                'timestamp': time.time()
            })
            
            risk_level = result['risk_level']
            risk_score = result['risk_score']
            
            if risk_level == "HIGH":
                st.error(f"🔴 **Risk Level: {risk_level}** (Score: {risk_score}/100)")
            elif risk_level == "MEDIUM":
                st.warning(f"🟡 **Risk Level: {risk_level}** (Score: {risk_score}/100)")
            else:
                st.success(f"🟢 **Risk Level: {risk_level}** (Score: {risk_score}/100)")
            
            st.json(result['factors'])
    
    with tab3:
        st.subheader("Anomaly Detection")
        
        st.info("Anomaly detection automatically runs when new blocks are added. Latest blocks are analyzed for suspicious patterns.")
        
        chain = blockchain.get_chain()
        if len(chain) > 1:
            latest_block = chain[-1]
            
            if st.button("🔍 Check Latest Block", type="primary"):
                with st.spinner("Analyzing for anomalies..."):
                    result = ai_module.detect_anomaly(latest_block)
                
                if result.get('is_anomaly'):
                    st.error("⚠️ **Anomaly Detected!**")
                    st.warning(f"Confidence: {result.get('confidence', 0):.4f}")
                    st.warning(f"Status: {result.get('status', 'Unknown')}")
                else:
                    st.success("✅ **No Anomaly Detected**")
                    st.info(f"Confidence: {result.get('confidence', 0):.4f}")
                    st.info(f"Status: {result.get('status', 'Unknown')}")
        else:
            st.warning("Add more blocks to use anomaly detection")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: white;'>
    <p>🔐 Blockchain + AI + Security System | Built with Streamlit, Python & Advanced Cryptography</p>
</div>
""", unsafe_allow_html=True)
