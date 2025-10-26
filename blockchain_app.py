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
    page_title="🔐 Blockchain Security Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Blockchain + AI + Security Platform v2.0"
    }
)

# Hide sidebar collapse button with JavaScript
st.markdown("""
<script>
    const hideCollapseButton = () => {
        const buttons = window.parent.document.querySelectorAll('button[kind="header"]');
        buttons.forEach(btn => btn.style.display = 'none');
    };
    hideCollapseButton();
    // Run again after a delay to ensure it catches dynamically loaded elements
    setTimeout(hideCollapseButton, 1000);
</script>
""", unsafe_allow_html=True)

# Professional CSS with modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 50%, #dce4f7 100%);
        background-attachment: fixed;
    }
    
    h1, h2, h3, h4 {
        color: #1a202c !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    p, label, span, div {
        color: #2d3748 !important;
    }
    
    /* Metric styling */
    div[data-testid="stMetricValue"] {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(45deg, #00d4ff, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #4a5568 !important;
        font-weight: 600;
        font-size: 15px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 2.5rem;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 20px rgba(66, 153, 225, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(66, 153, 225, 0.3) !important;
        border-radius: 12px !important;
        color: #2d3748 !important;
        padding: 12px !important;
        font-size: 15px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #4a5568 !important;
        font-weight: 600;
        padding: 12px 24px;
        font-size: 15px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(66, 153, 225, 0.15);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4299e1 0%, #667eea 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
        border-right: 2px solid rgba(66, 153, 225, 0.3);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 15px;
    }
    
    .stRadio label {
        padding: 12px;
        border-radius: 10px;
        transition: all 0.3s ease;
        color: #2d3748 !important;
    }
    
    .stRadio label:hover {
        background: rgba(66, 153, 225, 0.15);
    }
    
    /* Divider */
    hr {
        border-color: rgba(66, 153, 225, 0.3) !important;
        margin: 2rem 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(66, 153, 225, 0.12) !important;
        border-radius: 12px !important;
        color: #2d3748 !important;
        font-weight: 600 !important;
        padding: 15px !important;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(66, 153, 225, 0.2) !important;
    }
    
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        border: 2px solid rgba(66, 153, 225, 0.2);
    }
    
    /* Success/Error/Warning/Info boxes */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 2px solid rgba(66, 153, 225, 0.3) !important;
        padding: 1rem !important;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        border: 2px solid rgba(66, 153, 225, 0.25) !important;
    }
    
    .stCodeBlock code {
        color: #2d3748 !important;
    }
    
    /* Hide sidebar collapse button completely */
    button[kind="header"] {
        display: none !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    [data-testid="baseButton-header"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] button[kind="header"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child > button {
        display: none !important;
    }
    
    /* Hide the collapse arrow icon */
    .css-1544g2n, .css-163ttbj, .st-emotion-cache-1gwvy71 {
        display: none !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tooltips */
    .stTooltipIcon {
        color: #667eea !important;
    }
    
    /* Cards effect */
    div[data-testid="column"] > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    div[data-testid="column"] > div:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'blockchain' not in st.session_state:
    with st.spinner("🚀 Initializing Blockchain System..."):
        st.session_state.blockchain = Blockchain(difficulty=4)
        st.session_state.ai_module = AIModule()
        st.session_state.security = SecurityModule()
        st.session_state.ai_module.train_anomaly_detector(st.session_state.blockchain.get_chain())
        st.session_state.rsa_encrypted = None
        st.session_state.aes_data = {}
        st.session_state.signature = None
        st.session_state.initialized = True

blockchain = st.session_state.blockchain
ai_module = st.session_state.ai_module
security = st.session_state.security

# Header with animation
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <h1 style='font-size: 3.8rem; margin-bottom: 0.5rem; letter-spacing: 2px;'>
        🔐 BLOCKCHAIN SECURITY PLATFORM
    </h1>
    <p style='font-size: 1.4rem; color: #a0a0d0; margin-top: 0;'>
        Advanced Distributed Ledger • AI Analytics • Military-Grade Cryptography
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 SYSTEM STATUS")
    
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
        st.metric("❤️ Health", f"{health_score}%", delta="Excellent", delta_color="normal")
    elif health_score >= 60:
        st.metric("💛 Health", f"{health_score}%", delta="Good", delta_color="normal")
    else:
        st.metric("🔴 Health", f"{health_score}%", delta="Warning", delta_color="inverse")
    
    if stats['is_valid']:
        st.success("✅ Chain Valid")
    else:
        st.error("❌ Chain Invalid")
    
    st.divider()
    
    st.markdown("### 🧭 NAVIGATION")
    page = st.radio(
        "Navigation Menu",
        ["🏠 Dashboard", "⛓️ Blockchain", "🔐 Security Suite", "🤖 AI Analytics", "📈 Visualizations"],
        label_visibility="hidden"
    )
    
    st.divider()
    
    st.markdown("### ⏱️ LIVE STATS")
    analysis = ai_module.analyze_blockchain_patterns(chain)
    if 'total_blocks' in analysis and analysis['total_blocks'] > 1:
        st.metric("📊 Avg Nonce", f"{analysis['average_nonce']:.0f}")
        st.metric("⏱️ Avg Time", f"{analysis['avg_block_time']:.2f}s")
        st.caption(f"📈 Trend: {analysis['mining_difficulty_trend']}")

# Main Content
if page == "🏠 Dashboard":
    st.markdown("## 🏠 SYSTEM DASHBOARD")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Blocks", stats['total_blocks'], delta=f"+{stats['total_blocks']-1}")
    with col2:
        st.metric("Mining Difficulty", stats['difficulty'], delta="PoW Active")
    with col3:
        status = "🟢 SECURE" if stats['is_valid'] else "🔴 COMPROMISED"
        st.metric("Chain Status", status)
    with col4:
        st.metric("AI Health", f"{health['health_score']}%", delta="Monitored")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 MINING PERFORMANCE")
        if len(chain) > 1:
            block_indices = [b['index'] for b in chain]
            nonces = [b['nonce'] for b in chain]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=block_indices, y=nonces,
                mode='lines+markers',
                name='Nonce Value',
                line=dict(color='#667eea', width=4),
                marker=dict(size=12, color='#764ba2', line=dict(width=2, color='white'))
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.05)',
                font=dict(color='white', size=12),
                xaxis_title="Block Index",
                yaxis_title="Nonce Value",
                height=350,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 Mine more blocks to visualize trends")
    
    with col2:
        st.markdown("#### 🎯 HEALTH METRICS")
        categories = ['Chain Integrity', 'Block Count', 'AI Analysis']
        values = [
            100 if stats['is_valid'] else 0,
            min(stats['total_blocks'] * 10, 100),
            health_score
        ]
        
        fig = go.Figure(data=[go.Bar(
            x=categories, y=values,
            marker=dict(
                color=['#10b981', '#667eea', '#764ba2'],
                line=dict(width=2, color='white')
            ),
            text=[f"{v}%" for v in values],
            textposition='auto',
            textfont=dict(size=16, color='white', family='Poppins')
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.05)',
            font=dict(color='white', size=12),
            yaxis=dict(range=[0, 110]),
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.markdown("#### 🔗 RECENT BLOCKS")
    
    if len(chain) > 1:
        recent_blocks = chain[-5:][::-1]
        for idx, block in enumerate(recent_blocks):
            col1, col2, col3, col4, col5 = st.columns([1, 2, 1.5, 1.5, 0.8])
            with col1:
                if block['index'] == 0:
                    st.markdown("🌟 **Genesis**")
                else:
                    st.markdown(f"**Block #{block['index']}**")
            with col2:
                st.markdown(f"`{block['hash'][:28]}...`")
            with col3:
                st.markdown(f"⛏️ Nonce: **{block['nonce']}**")
            with col4:
                ts = datetime.fromtimestamp(block['timestamp'])
                st.markdown(f"🕐 {ts.strftime('%H:%M:%S')}")
            with col5:
                anomaly = ai_module.detect_anomaly(block)
                st.markdown("⚠️" if anomaly.get('is_anomaly') else "✅")
            
            if idx < len(recent_blocks) - 1:
                st.divider()
    else:
        st.info("💡 Add blocks to see them here")
    
    st.divider()
    st.markdown("#### ⚡ QUICK ACTIONS")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⛏️ MINE BLOCK", use_container_width=True):
            try:
                with st.spinner("Mining..."):
                    new_block = blockchain.add_block({"type": "quick_mine", "timestamp": time.time()})
                    ai_module.train_anomaly_detector(blockchain.get_chain())
                st.success(f"✅ Block #{new_block.index} mined!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("✅ VALIDATE CHAIN", use_container_width=True):
            with st.spinner("Validating..."):
                is_valid = blockchain.is_chain_valid()
            if is_valid:
                st.success("✅ Chain is valid!")
            else:
                st.error("❌ Chain validation failed!")
    
    with col3:
        if st.button("🤖 RUN AI SCAN", use_container_width=True):
            with st.spinner("Analyzing..."):
                analysis = ai_module.analyze_blockchain_patterns(chain)
            st.info(f"📊 Trend: {analysis.get('mining_difficulty_trend', 'N/A')}")
    
    with col4:
        if st.button("🔄 REFRESH DATA", use_container_width=True):
            st.rerun()

elif page == "⛓️ Blockchain":
    st.markdown("## ⛓️ BLOCKCHAIN MANAGEMENT")
    
    tab1, tab2 = st.tabs(["➕ MINE NEW BLOCK", "📋 BLOCKCHAIN EXPLORER"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### ⛏️ Create Transaction")
            
            template = st.selectbox(
                "📑 Select Template",
                ["Custom JSON", "💸 Simple Transfer", "📜 Smart Contract", "📊 Data Record"],
                index=1
            )
            
            if template == "💸 Simple Transfer":
                sender = st.text_input("👤 Sender", "Alice", key="sender")
                receiver = st.text_input("👤 Receiver", "Bob", key="receiver")
                amount = st.number_input("💰 Amount", min_value=0, value=100, step=10)
                transaction_data = json.dumps({
                    "type": "transfer",
                    "sender": sender,
                    "receiver": receiver,
                    "amount": amount,
                    "timestamp": time.time()
                })
            elif template == "📜 Smart Contract":
                contract = st.text_input("📝 Contract Name", "TokenContract")
                action = st.selectbox("⚡ Action", ["deploy", "execute", "query"])
                transaction_data = json.dumps({
                    "type": "smart_contract",
                    "name": contract,
                    "action": action,
                    "timestamp": time.time()
                })
            elif template == "📊 Data Record":
                record_type = st.text_input("📁 Record Type", "UserData")
                data_input = st.text_area("📄 Data (JSON)", '{"name": "John", "value": 100}', height=100)
                try:
                    data_json = json.loads(data_input)
                    transaction_data = json.dumps({
                        "type": "data_record",
                        "record_type": record_type,
                        "data": data_json,
                        "timestamp": time.time()
                    })
                except:
                    transaction_data = json.dumps({"type": "data_record", "error": "Invalid JSON"})
            else:
                transaction_data = st.text_area(
                    "📝 Transaction Data (JSON)",
                    value='{"sender": "Alice", "receiver": "Bob", "amount": 100}',
                    height=180
                )
            
            st.divider()
            
            if st.button("⛏️ MINE BLOCK NOW", type="primary", use_container_width=True):
                try:
                    data = json.loads(transaction_data)
                    
                    progress_text = "🔨 Mining block... Please wait"
                    progress_bar = st.progress(0, text=progress_text)
                    
                    start_time = time.time()
                    new_block = blockchain.add_block(data)
                    mining_time = time.time() - start_time
                    
                    progress_bar.progress(100, text="✅ Block mined successfully!")
                    
                    ai_module.train_anomaly_detector(blockchain.get_chain())
                    anomaly = ai_module.detect_anomaly(new_block.to_dict())
                    
                    st.success(f"✅ **Block #{new_block.index} mined in {mining_time:.2f} seconds!**")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.info(f"**🔐 Hash:** `{new_block.hash[:35]}...`")
                        st.info(f"**⛏️ Nonce:** {new_block.nonce:,}")
                    with col_b:
                        ts = datetime.fromtimestamp(new_block.timestamp)
                        st.info(f"**🕐 Time:** {ts.strftime('%Y-%m-%d %H:%M:%S')}")
                        if anomaly.get('is_anomaly'):
                            st.warning("⚠️ **Anomaly Detected**")
                        else:
                            st.success("✅ **Normal Block**")
                    
                    time.sleep(1.5)
                    st.rerun()
                    
                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format. Please check your input.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with col2:
            st.markdown("### 📊 MINING STATISTICS")
            
            if 'total_blocks' in analysis and analysis['total_blocks'] > 1:
                st.metric("🎯 Average Nonce", f"{analysis['average_nonce']:,.0f}")
                st.metric("⚡ Maximum Nonce", f"{analysis['max_nonce']:,}")
                st.metric("⏱️ Average Time", f"{analysis['avg_block_time']:.2f}s")
                
                trend = analysis['mining_difficulty_trend']
                if trend == "Increasing":
                    st.error(f"📈 Trend: {trend}")
                elif trend == "Decreasing":
                    st.success(f"📉 Trend: {trend}")
                else:
                    st.info(f"➡️ Trend: {trend}")
                
                if len(chain) > 3:
                    st.markdown("#### 📊 Nonce Distribution")
                    nonces = [b['nonce'] for b in chain if b['index'] > 0]
                    fig = go.Figure(data=[go.Histogram(
                        x=nonces,
                        nbinsx=15,
                        marker_color='#667eea',
                        marker_line=dict(width=2, color='white')
                    )])
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(255,255,255,0.05)',
                        font=dict(color='white'),
                        height=250,
                        showlegend=False,
                        xaxis_title="Nonce Value",
                        yaxis_title="Frequency"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Mine more blocks for detailed statistics")
    
    with tab2:
        st.markdown("### 📋 EXPLORE BLOCKCHAIN")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search by hash or index", "", placeholder="Enter hash or block number")
        with col2:
            sort_order = st.selectbox("📊 Sort Order", ["Newest First", "Oldest First"])
        with col3:
            if st.button("🔄 REFRESH", use_container_width=True):
                st.rerun()
        
        display_chain = chain[::-1] if sort_order == "Newest First" else chain
        
        if search:
            display_chain = [b for b in display_chain if search.lower() in str(b['hash']).lower() or search in str(b['index'])]
        
        st.markdown(f"**📊 Showing {len(display_chain)} of {len(chain)} blocks**")
        st.divider()
        
        for block in display_chain:
            with st.expander(f"{'🌟' if block['index'] == 0 else '🔗'} Block #{block['index']} - `{block['hash'][:25]}...`", expanded=(block['index'] == len(chain)-1 and not search)):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**📍 Index:** {block['index']}")
                    ts = datetime.fromtimestamp(block['timestamp'])
                    st.markdown(f"**🕐 Timestamp:** {ts.strftime('%Y-%m-%d %H:%M:%S')}")
                    st.markdown(f"**⛏️ Nonce:** {block['nonce']:,}")
                
                with col2:
                    st.markdown(f"**🔐 Hash:**")
                    st.code(block['hash'], language="text")
                    st.markdown(f"**🔗 Previous Hash:**")
                    st.code(block['previous_hash'], language="text")
                
                st.markdown("**📄 Transaction Data:**")
                st.json(block['data'])

elif page == "🔐 Security Suite":
    st.markdown("## 🔐 CRYPTOGRAPHIC SECURITY SUITE")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔢 HASHING", "🔒 RSA ENCRYPTION", "🔐 AES ENCRYPTION", "✍️ DIGITAL SIGNATURES"])
    
    with tab1:
        st.markdown("### 🔢 CRYPTOGRAPHIC HASHING")
        col1, col2 = st.columns([3, 1])
        with col1:
            hash_input = st.text_input("📝 Data to Hash", "Hello Blockchain Security", key="hash_input")
        with col2:
            algo = st.selectbox("⚙️ Algorithm", ["sha256", "sha512", "md5"])
        
        if st.button("🔐 GENERATE HASH", use_container_width=True):
            with st.spinner("Hashing..."):
                hashed = security.hash_data(hash_input, algo)
            st.success(f"✅ Hash generated using {algo.upper()}!")
            st.code(hashed, language="text")
            st.info(f"**📏 Length:** {len(hashed)} characters")
    
    with tab2:
        st.markdown("### 🔒 RSA ENCRYPTION (2048-bit)")
        rsa_input = st.text_input("📝 Data to Encrypt/Decrypt", "Top Secret Message", key="rsa_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔒 ENCRYPT WITH RSA", type="primary", use_container_width=True):
                with st.spinner("Encrypting..."):
                    encrypted = security.rsa_encrypt(rsa_input)
                    st.session_state.rsa_encrypted = encrypted
                st.success("✅ Data encrypted successfully!")
                st.code(encrypted[:100] + "..." if len(encrypted) > 100 else encrypted, language="text")
                st.info(f"**📏 Ciphertext Length:** {len(encrypted)} characters")
        
        with col2:
            if st.button("🔓 DECRYPT WITH RSA", use_container_width=True):
                if st.session_state.rsa_encrypted:
                    with st.spinner("Decrypting..."):
                        decrypted = security.rsa_decrypt(st.session_state.rsa_encrypted)
                    st.success("✅ Data decrypted successfully!")
                    st.code(decrypted, language="text")
                else:
                    st.warning("⚠️ Please encrypt data first!")
    
    with tab3:
        st.markdown("### 🔐 AES ENCRYPTION (256-bit CBC)")
        aes_input = st.text_input("📝 Data to Encrypt/Decrypt", "Confidential Information", key="aes_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 ENCRYPT WITH AES", type="primary", use_container_width=True):
                with st.spinner("Encrypting..."):
                    result = security.aes_encrypt(aes_input)
                    st.session_state.aes_data = result
                st.success("✅ Data encrypted successfully!")
                st.code(result['ciphertext'][:80] + "..." if len(result['ciphertext']) > 80 else result['ciphertext'], language="text")
                with st.expander("🔑 View Encryption Keys"):
                    st.text(f"🔑 Key: {result['key'][:50]}...")
                    st.text(f"🎲 IV: {result['iv']}")
        
        with col2:
            if st.button("🔓 DECRYPT WITH AES", use_container_width=True):
                if st.session_state.aes_data:
                    with st.spinner("Decrypting..."):
                        decrypted = security.aes_decrypt(
                            st.session_state.aes_data['ciphertext'],
                            st.session_state.aes_data['key'],
                            st.session_state.aes_data['iv']
                        )
                    st.success("✅ Data decrypted successfully!")
                    st.code(decrypted, language="text")
                else:
                    st.warning("⚠️ Please encrypt data first!")
    
    with tab4:
        st.markdown("### ✍️ ECDSA DIGITAL SIGNATURES (Secp256k1)")
        sign_input = st.text_input("📝 Document to Sign", "Important Legal Document", key="sign_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✍️ SIGN DOCUMENT", type="primary", use_container_width=True):
                with st.spinner("Signing..."):
                    signature = security.sign_data(sign_input)
                    st.session_state.signature = signature
                st.success("✅ Document signed successfully!")
                st.code(signature, language="text")
                st.info("**🔐 Signature Algorithm:** ECDSA-Secp256k1")
        
        with col2:
            if st.button("✅ VERIFY SIGNATURE", use_container_width=True):
                if st.session_state.signature:
                    with st.spinner("Verifying..."):
                        is_valid = security.verify_signature(sign_input, st.session_state.signature)
                    if is_valid:
                        st.success("✅ **SIGNATURE IS VALID!**")
                        st.balloons()
                    else:
                        st.error("❌ **SIGNATURE IS INVALID!**")
                else:
                    st.warning("⚠️ Please sign document first!")

elif page == "🤖 AI Analytics":
    st.markdown("## 🤖 ARTIFICIAL INTELLIGENCE ANALYTICS")
    
    tab1, tab2, tab3 = st.tabs(["📊 PATTERN ANALYSIS", "⚠️ RISK ASSESSMENT", "🔍 ANOMALY DETECTION"])
    
    with tab1:
        st.markdown("### 📊 BLOCKCHAIN PATTERN ANALYSIS")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔍 ANALYZE BLOCKCHAIN", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is analyzing blockchain patterns..."):
                    time.sleep(0.5)
                    analysis = ai_module.analyze_blockchain_patterns(chain)
                
                st.success("✅ Analysis complete!")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("📦 Total Blocks", analysis.get('total_blocks', 0))
                    st.metric("📊 Avg Nonce", f"{analysis.get('average_nonce', 0):,.0f}")
                with col_b:
                    st.metric("⚡ Max Nonce", f"{analysis.get('max_nonce', 0):,}")
                    st.metric("⏬ Min Nonce", f"{analysis.get('min_nonce', 0):,}")
                with col_c:
                    st.metric("⏱️ Avg Time", f"{analysis.get('avg_block_time', 0):.2f}s")
                    trend = analysis.get('mining_difficulty_trend', 'N/A')
                    st.info(f"**📈 Trend:** {trend}")
        
        with col2:
            if st.button("🧠 RETRAIN AI MODEL", use_container_width=True):
                with st.spinner("🧠 Training AI model..."):
                    result = ai_module.train_anomaly_detector(chain)
                
                if result['status'] == 'success':
                    st.success(f"✅ Model trained with {result['samples_trained']} samples!")
                else:
                    st.error(f"❌ Training failed: {result['message']}")
    
    with tab2:
        st.markdown("### ⚠️ TRANSACTION RISK ASSESSMENT")
        
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("💰 Transaction Amount", min_value=0, value=5000, step=100, key="risk_amount")
        with col2:
            data = st.text_input("📝 Transaction Data", "Large wire transfer", key="risk_data")
        
        if st.button("🎯 ASSESS RISK LEVEL", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is assessing risk..."):
                result = ai_module.predict_transaction_risk({
                    'amount': amount,
                    'data': data,
                    'timestamp': time.time()
                })
            
            risk_level = result['risk_level']
            risk_score = result['risk_score']
            
            if risk_level == "HIGH":
                st.error(f"🔴 **RISK LEVEL: {risk_level}** (Score: {risk_score}/100)")
            elif risk_level == "MEDIUM":
                st.warning(f"🟡 **RISK LEVEL: {risk_level}** (Score: {risk_score}/100)")
            else:
                st.success(f"🟢 **RISK LEVEL: {risk_level}** (Score: {risk_score}/100)")
            
            st.markdown("**📋 Risk Factors:**")
            st.json(result['factors'])
    
    with tab3:
        st.markdown("### 🔍 ANOMALY DETECTION")
        
        st.info("💡 **AI automatically analyzes each new block for anomalies using Isolation Forest algorithm**")
        
        if len(chain) > 1:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("🔍 CHECK LATEST BLOCK", type="primary", use_container_width=True):
                    with st.spinner("🤖 AI is detecting anomalies..."):
                        result = ai_module.detect_anomaly(chain[-1])
                    
                    if result.get('is_anomaly'):
                        st.error("⚠️ **ANOMALY DETECTED IN LATEST BLOCK!**")
                        st.warning(f"**🎯 Confidence:** {result.get('confidence', 0):.4f}")
                        st.warning(f"**📊 Status:** {result.get('status', 'Unknown')}")
                    else:
                        st.success("✅ **NO ANOMALY DETECTED**")
                        st.info(f"**🎯 Confidence:** {result.get('confidence', 0):.4f}")
                        st.info(f"**📊 Status:** {result.get('status', 'Unknown')}")
            
            with col2:
                if st.button("🔍 SCAN ALL BLOCKS", use_container_width=True):
                    with st.spinner("🤖 Scanning entire blockchain..."):
                        anomaly_count = 0
                        for block in chain:
                            result = ai_module.detect_anomaly(block)
                            if result.get('is_anomaly'):
                                anomaly_count += 1
                    
                    if anomaly_count > 0:
                        st.warning(f"⚠️ **Found {anomaly_count} anomalous block(s)**")
                    else:
                        st.success("✅ **All blocks are normal**")
        else:
            st.warning("⚠️ Add more blocks to enable anomaly detection")

else:  # Visualizations
    st.markdown("## 📈 ADVANCED DATA VISUALIZATIONS")
    
    if len(chain) > 2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔗 BLOCKCHAIN NETWORK GRAPH")
            fig = go.Figure()
            
            for i, block in enumerate(chain):
                fig.add_trace(go.Scatter(
                    x=[i], y=[block['nonce']],
                    mode='markers+text',
                    marker=dict(
                        size=30,
                        color='#667eea' if i > 0 else '#10b981',
                        line=dict(width=3, color='white')
                    ),
                    text=[f"B{i}"],
                    textposition="top center",
                    textfont=dict(size=14, color='white', family='Poppins'),
                    name=f"Block {i}",
                    hovertemplate=f"<b>Block {i}</b><br>Nonce: {block['nonce']}<br>Hash: {block['hash'][:20]}...<extra></extra>"
                ))
            
            # Add connections
            for i in range(1, len(chain)):
                fig.add_trace(go.Scatter(
                    x=[i-1, i], y=[chain[i-1]['nonce'], chain[i]['nonce']],
                    mode='lines',
                    line=dict(color='rgba(102, 126, 234, 0.5)', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.05)',
                font=dict(color='white', family='Poppins'),
                showlegend=False,
                height=450,
                xaxis_title="Block Index",
                yaxis_title="Nonce Value"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### ⏱️ MINING TIME ANALYSIS")
            if len(chain) > 2:
                times = []
                block_nums = []
                for i in range(1, len(chain)):
                    time_diff = chain[i]['timestamp'] - chain[i-1]['timestamp']
                    times.append(time_diff)
                    block_nums.append(f"B{i-1}→B{i}")
                
                fig = go.Figure()
                fig.add_trace(go.Box(
                    y=times,
                    name='Mining Time',
                    marker_color='#764ba2',
                    boxmean='sd'
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(255,255,255,0.05)',
                    font=dict(color='white', family='Poppins'),
                    yaxis_title="Time (seconds)",
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 NONCE PROGRESSION")
            nonces = [b['nonce'] for b in chain]
            indices = [b['index'] for b in chain]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=indices, y=nonces,
                marker=dict(
                    color=nonces,
                    colorscale='Viridis',
                    line=dict(width=2, color='white')
                ),
                text=nonces,
                textposition='outside',
                textfont=dict(size=12, color='white')
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.05)',
                font=dict(color='white', family='Poppins'),
                height=400,
                xaxis_title="Block Index",
                yaxis_title="Nonce Value"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 HASH DISTRIBUTION")
            # Analyze hash patterns
            hash_starts = [int(b['hash'][:2], 16) for b in chain if b['index'] > 0]
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=hash_starts,
                nbinsx=20,
                marker=dict(
                    color='#667eea',
                    line=dict(width=2, color='white')
                )
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.05)',
                font=dict(color='white', family='Poppins'),
                height=400,
                xaxis_title="Hash Prefix Value",
                yaxis_title="Frequency"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 **Mine at least 3 blocks to unlock advanced visualizations**")
        
        if st.button("⛏️ QUICK MINE 5 BLOCKS", type="primary"):
            with st.spinner("⛏️ Mining 5 blocks..."):
                for i in range(5):
                    blockchain.add_block({"type": "auto_mine", "index": i})
                ai_module.train_anomaly_detector(blockchain.get_chain())
            st.success("✅ Successfully mined 5 blocks!")
            time.sleep(1)
            st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #b8b8d4; padding: 1.5rem 0;'>
    <p style='font-size: 1.1rem; margin: 0;'>
        🔐 <strong>Blockchain Security Platform v2.0</strong> | 
        Built with <span style='color: #e74c3c;'>❤️</span> using Python, Streamlit & Advanced Cryptography
    </p>
    <p style='font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;'>
        🔒 Secure | 🤖 Intelligent | 🎨 Beautiful
    </p>
</div>
""", unsafe_allow_html=True)
