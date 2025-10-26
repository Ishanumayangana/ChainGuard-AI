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

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    p, label, span {
        color: #e0e0e0 !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(103, 126, 234, 0.8);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #b8b8d4 !important;
        font-weight: 600;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #b8b8d4 !important;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
    }
    
    hr {
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
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

blockchain = st.session_state.blockchain
ai_module = st.session_state.ai_module
security = st.session_state.security

# Title
st.markdown("""
<div style='text-align: center; padding: 1.5rem 0;'>
    <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🔐 Blockchain + AI + Security</h1>
    <p style='font-size: 1.2rem; color: #b8b8d4; margin-top: 0.5rem;'>
        Advanced Distributed Ledger Technology with AI-Powered Analytics & Military-Grade Cryptography
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Live System Metrics")
    
    stats = blockchain.get_chain_stats()
    chain = blockchain.get_chain()
    health = ai_module.get_blockchain_health_score(chain, stats['is_valid'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔗 Blocks", stats['total_blocks'])
    with col2:
        st.metric("⚡ Difficulty", stats['difficulty'])
    
    health_score = health['health_score']
    if health_score >= 80:
        st.metric("❤️ Health", f"{health_score}%", delta="Excellent")
    elif health_score >= 60:
        st.metric("💛 Health", f"{health_score}%", delta="Good")
    else:
        st.metric("🔴 Health", f"{health_score}%", delta="Check")
    
    if stats['is_valid']:
        st.success("✅ Chain Valid")
    else:
        st.error("❌ Chain Invalid")
    
    st.divider()
    
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "Select Page",
        ["🏠 Dashboard", "⛓️ Blockchain", "🔐 Security Suite", "🤖 AI Analytics", "📈 Visualizations"],
        label_visibility="hidden"
    )
    
    st.divider()
    
    st.markdown("### ⏱️ Real-Time Stats")
    analysis = ai_module.analyze_blockchain_patterns(chain)
    if 'total_blocks' in analysis and analysis['total_blocks'] > 1:
        st.metric("📊 Avg Nonce", f"{analysis['average_nonce']:.0f}")
        st.metric("⏱️ Avg Time", f"{analysis['avg_block_time']:.2f}s")

# Main Content
if page == "🏠 Dashboard":
    st.markdown("## 🏠 System Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Blocks", stats['total_blocks'], delta=f"+{stats['total_blocks']-1} mined")
    with col2:
        st.metric("Mining Difficulty", stats['difficulty'], delta="PoW")
    with col3:
        st.metric("Chain Status", "SECURE" if stats['is_valid'] else "COMPROMISED")
    with col4:
        st.metric("AI Health", f"{health['health_score']}%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Block Mining Trends")
        if len(chain) > 1:
            block_indices = [b['index'] for b in chain]
            nonces = [b['nonce'] for b in chain]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=block_indices, y=nonces,
                mode='lines+markers',
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
            st.info("Add more blocks to see trends")
    
    with col2:
        st.markdown("#### 🎯 System Health")
        categories = ['Chain', 'Blocks', 'AI']
        values = [
            100 if stats['is_valid'] else 0,
            min(stats['total_blocks'] * 10, 100),
            health_score
        ]
        
        fig = go.Figure(data=[go.Bar(
            x=categories, y=values,
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
    st.markdown("#### 🔗 Recent Blocks")
    
    if len(chain) > 1:
        recent_blocks = chain[-5:][::-1]
        for block in recent_blocks:
            col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
            with col1:
                st.markdown(f"**Block #{block['index']}**")
            with col2:
                st.markdown(f"`{block['hash'][:25]}...`")
            with col3:
                st.markdown(f"Nonce: {block['nonce']}")
            with col4:
                anomaly = ai_module.detect_anomaly(block)
                st.markdown("⚠️" if anomaly.get('is_anomaly') else "✅")
            st.divider()

elif page == "⛓️ Blockchain":
    st.markdown("## ⛓️ Blockchain Management")
    
    tab1, tab2 = st.tabs(["➕ Add Block", "📋 View Chain"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### ⛏️ Mine New Block")
            
            template = st.selectbox("Template:", ["Custom JSON", "Simple Transfer", "Smart Contract"])
            
            if template == "Simple Transfer":
                sender = st.text_input("Sender:", "Alice")
                receiver = st.text_input("Receiver:", "Bob")
                amount = st.number_input("Amount:", min_value=0, value=100)
                transaction_data = json.dumps({"sender": sender, "receiver": receiver, "amount": amount})
            elif template == "Smart Contract":
                contract = st.text_input("Contract:", "TokenContract")
                action = st.selectbox("Action:", ["deploy", "execute"])
                transaction_data = json.dumps({"type": "smart_contract", "name": contract, "action": action})
            else:
                transaction_data = st.text_area(
                    "Transaction Data (JSON):",
                    value='{"sender": "Alice", "receiver": "Bob", "amount": 100}',
                    height=120
                )
            
            if st.button("⛏️ Mine Block", type="primary", use_container_width=True):
                try:
                    data = json.loads(transaction_data)
                    progress_bar = st.progress(0, text="Mining block... 🔨")
                    
                    start_time = time.time()
                    new_block = blockchain.add_block(data)
                    mining_time = time.time() - start_time
                    
                    progress_bar.progress(100, text="Mined! ✅")
                    
                    ai_module.train_anomaly_detector(blockchain.get_chain())
                    anomaly = ai_module.detect_anomaly(new_block.to_dict())
                    
                    st.success(f"✅ Block #{new_block.index} mined in {mining_time:.2f}s!")
                    st.info(f"**Hash:** `{new_block.hash[:40]}...`")
                    st.info(f"**Nonce:** {new_block.nonce}")
                    
                    if anomaly.get('is_anomaly'):
                        st.warning("⚠️ Anomaly detected!")
                    
                    time.sleep(1)
                    st.rerun()
                    
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with col2:
            st.markdown("### 📊 Mining Stats")
            if 'total_blocks' in analysis and analysis['total_blocks'] > 1:
                st.metric("Avg Nonce", f"{analysis['average_nonce']:.0f}")
                st.metric("Max Nonce", analysis['max_nonce'])
                st.metric("Avg Time", f"{analysis['avg_block_time']:.2f}s")
            else:
                st.info("Mine more blocks for stats")
    
    with tab2:
        st.markdown("### 📋 Blockchain Explorer")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("🔍 Search:", "")
        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        for block in chain[::-1]:
            if search and search.lower() not in str(block['hash']).lower() and search not in str(block['index']):
                continue
            
            with st.expander(f"🔗 Block #{block['index']} - {block['hash'][:20]}...", expanded=(block['index'] == len(chain)-1)):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Index:** {block['index']}")
                    st.markdown(f"**Nonce:** {block['nonce']}")
                with col2:
                    ts = datetime.fromtimestamp(block['timestamp'])
                    st.markdown(f"**Time:** {ts.strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**Hash:** `{block['hash']}`")
                st.markdown(f"**Previous:** `{block['previous_hash']}`")
                st.json(block['data'])

elif page == "🔐 Security Suite":
    st.markdown("## 🔐 Security & Cryptography Tools")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔢 Hashing", "🔒 RSA", "🔐 AES", "✍️ Signatures"])
    
    with tab1:
        st.markdown("### 🔢 Cryptographic Hashing")
        col1, col2 = st.columns([3, 1])
        with col1:
            hash_input = st.text_input("Data:", "Hello Blockchain")
        with col2:
            algo = st.selectbox("Algorithm:", ["sha256", "sha512", "md5"])
        
        if st.button("Generate Hash", use_container_width=True):
            hashed = security.hash_data(hash_input, algo)
            st.success("✅ Hash generated!")
            st.code(hashed, language="text")
    
    with tab2:
        st.markdown("### 🔒 RSA Encryption (2048-bit)")
        rsa_input = st.text_input("Data:", "Secret Message", key="rsa")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔒 Encrypt", type="primary", use_container_width=True):
                encrypted = security.rsa_encrypt(rsa_input)
                st.session_state.rsa_encrypted = encrypted
                st.success("Encrypted!")
                st.code(encrypted[:80] + "...", language="text")
        
        with col2:
            if st.button("🔓 Decrypt", use_container_width=True):
                if st.session_state.rsa_encrypted:
                    decrypted = security.rsa_decrypt(st.session_state.rsa_encrypted)
                    st.success("Decrypted!")
                    st.code(decrypted, language="text")
                else:
                    st.warning("Encrypt data first!")
    
    with tab3:
        st.markdown("### 🔐 AES Encryption (256-bit CBC)")
        aes_input = st.text_input("Data:", "Confidential", key="aes")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔒 Encrypt AES", type="primary", use_container_width=True):
                result = security.aes_encrypt(aes_input)
                st.session_state.aes_data = result
                st.success("Encrypted!")
                st.code(result['ciphertext'][:60] + "...", language="text")
        
        with col2:
            if st.button("🔓 Decrypt AES", use_container_width=True):
                if st.session_state.aes_data:
                    decrypted = security.aes_decrypt(
                        st.session_state.aes_data['ciphertext'],
                        st.session_state.aes_data['key'],
                        st.session_state.aes_data['iv']
                    )
                    st.success("Decrypted!")
                    st.code(decrypted, language="text")
                else:
                    st.warning("Encrypt data first!")
    
    with tab4:
        st.markdown("### ✍️ ECDSA Digital Signatures")
        sign_input = st.text_input("Data to sign:", "Important Doc", key="sign")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✍️ Sign", type="primary", use_container_width=True):
                signature = security.sign_data(sign_input)
                st.session_state.signature = signature
                st.success("Signed!")
                st.code(signature, language="text")
        
        with col2:
            if st.button("✅ Verify", use_container_width=True):
                if st.session_state.signature:
                    is_valid = security.verify_signature(sign_input, st.session_state.signature)
                    if is_valid:
                        st.success("✅ Signature VALID!")
                    else:
                        st.error("❌ Signature INVALID!")
                else:
                    st.warning("Sign data first!")

elif page == "🤖 AI Analytics":
    st.markdown("## 🤖 AI/ML Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "⚠️ Risk Assessment", "🔍 Anomaly Detection"])
    
    with tab1:
        st.markdown("### 📊 Blockchain Pattern Analysis")
        
        if st.button("🔍 Analyze", type="primary", use_container_width=True):
            with st.spinner("Analyzing..."):
                analysis = ai_module.analyze_blockchain_patterns(chain)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Blocks", analysis.get('total_blocks', 0))
                st.metric("Avg Nonce", f"{analysis.get('average_nonce', 0):.2f}")
            with col2:
                st.metric("Max Nonce", analysis.get('max_nonce', 0))
                st.metric("Min Nonce", analysis.get('min_nonce', 0))
            with col3:
                st.metric("Avg Block Time", f"{analysis.get('avg_block_time', 0):.2f}s")
                st.info(f"Trend: {analysis.get('mining_difficulty_trend', 'N/A')}")
    
    with tab2:
        st.markdown("### ⚠️ Transaction Risk Assessment")
        
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Amount:", min_value=0, value=5000, step=100)
        with col2:
            data = st.text_input("Data:", "Large transfer")
        
        if st.button("🎯 Assess Risk", type="primary", use_container_width=True):
            result = ai_module.predict_transaction_risk({
                'amount': amount,
                'data': data,
                'timestamp': time.time()
            })
            
            risk_level = result['risk_level']
            risk_score = result['risk_score']
            
            if risk_level == "HIGH":
                st.error(f"🔴 Risk: {risk_level} ({risk_score}/100)")
            elif risk_level == "MEDIUM":
                st.warning(f"🟡 Risk: {risk_level} ({risk_score}/100)")
            else:
                st.success(f"🟢 Risk: {risk_level} ({risk_score}/100)")
            
            st.json(result['factors'])
    
    with tab3:
        st.markdown("### 🔍 Anomaly Detection")
        
        if len(chain) > 1:
            if st.button("🔍 Check Latest Block", type="primary", use_container_width=True):
                with st.spinner("Analyzing..."):
                    result = ai_module.detect_anomaly(chain[-1])
                
                if result.get('is_anomaly'):
                    st.error("⚠️ **Anomaly Detected!**")
                    st.warning(f"Confidence: {result.get('confidence', 0):.4f}")
                else:
                    st.success("✅ **No Anomaly**")
                    st.info(f"Confidence: {result.get('confidence', 0):.4f}")
        else:
            st.info("Add more blocks for analysis")

else:  # Visualizations
    st.markdown("## 📈 Advanced Visualizations")
    
    if len(chain) > 2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔗 Block Network")
            # Create network graph
            fig = go.Figure()
            
            for i, block in enumerate(chain):
                fig.add_trace(go.Scatter(
                    x=[i], y=[block['nonce']],
                    mode='markers+text',
                    marker=dict(size=20, color='#667eea'),
                    text=[f"B{i}"],
                    textposition="top center",
                    name=f"Block {i}"
                ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.05)',
                font=dict(color='white'),
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### ⏱️ Mining Time Distribution")
            if len(chain) > 2:
                times = []
                for i in range(1, len(chain)):
                    time_diff = chain[i]['timestamp'] - chain[i-1]['timestamp']
                    times.append(time_diff)
                
                fig = go.Figure(data=[go.Box(y=times, marker_color='#764ba2')])
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(255,255,255,0.05)',
                    font=dict(color='white'),
                    yaxis_title="Time (seconds)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add more blocks to see visualizations")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #b8b8d4; padding: 1rem;'>
    <p>🔐 Blockchain + AI + Security Platform | Built with Streamlit & Advanced Cryptography</p>
</div>
""", unsafe_allow_html=True)
