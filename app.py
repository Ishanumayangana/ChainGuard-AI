from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from blockchain import Blockchain, SecurityModule
from ai_module import AIModule
import json
import os
import logging

app = Flask(__name__, static_folder='static')
CORS(app)

# Disable Flask request logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Initialize blockchain and AI module
blockchain = Blockchain(difficulty=4)
ai_module = AIModule()
security = SecurityModule()

# Train AI module with initial blockchain data
ai_module.train_anomaly_detector(blockchain.get_chain())


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')


@app.route('/api/blockchain', methods=['GET'])
def get_blockchain():
    """Get the entire blockchain"""
    chain = blockchain.get_chain()
    stats = blockchain.get_chain_stats()
    
    return jsonify({
        'chain': chain,
        'stats': stats
    })


@app.route('/api/block/add', methods=['POST'])
def add_block():
    """Add a new block to the blockchain"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Add block to blockchain
        new_block = blockchain.add_block(data)
        
        # Retrain AI model with updated blockchain
        ai_module.train_anomaly_detector(blockchain.get_chain())
        
        # Check for anomalies
        anomaly_result = ai_module.detect_anomaly(new_block.to_dict())
        
        return jsonify({
            'success': True,
            'block': new_block.to_dict(),
            'anomaly_check': anomaly_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate', methods=['GET'])
def validate_chain():
    """Validate the blockchain"""
    is_valid = blockchain.is_chain_valid()
    health_score = ai_module.get_blockchain_health_score(
        blockchain.get_chain(),
        is_valid
    )
    
    return jsonify({
        'is_valid': is_valid,
        'health': health_score
    })


@app.route('/api/security/hash', methods=['POST'])
def hash_data():
    """Hash data using specified algorithm"""
    data = request.json.get('data', '')
    algorithm = request.json.get('algorithm', 'sha256')
    
    hashed = security.hash_data(data, algorithm)
    
    return jsonify({
        'original': data,
        'algorithm': algorithm,
        'hash': hashed
    })


@app.route('/api/security/encrypt/rsa', methods=['POST'])
def encrypt_rsa():
    """Encrypt data using RSA"""
    data = request.json.get('data', '')
    
    encrypted = security.rsa_encrypt(data)
    
    return jsonify({
        'original': data,
        'encrypted': encrypted,
        'method': 'RSA-2048'
    })


@app.route('/api/security/decrypt/rsa', methods=['POST'])
def decrypt_rsa():
    """Decrypt data using RSA"""
    encrypted_data = request.json.get('encrypted', '')
    
    decrypted = security.rsa_decrypt(encrypted_data)
    
    return jsonify({
        'encrypted': encrypted_data,
        'decrypted': decrypted,
        'method': 'RSA-2048'
    })


@app.route('/api/security/encrypt/aes', methods=['POST'])
def encrypt_aes():
    """Encrypt data using AES"""
    data = request.json.get('data', '')
    
    result = security.aes_encrypt(data)
    
    return jsonify({
        'original': data,
        'encrypted': result['ciphertext'],
        'key': result['key'],
        'iv': result['iv'],
        'method': 'AES-256-CBC'
    })


@app.route('/api/security/decrypt/aes', methods=['POST'])
def decrypt_aes():
    """Decrypt data using AES"""
    ciphertext = request.json.get('ciphertext', '')
    key = request.json.get('key', '')
    iv = request.json.get('iv', '')
    
    decrypted = security.aes_decrypt(ciphertext, key, iv)
    
    return jsonify({
        'encrypted': ciphertext,
        'decrypted': decrypted,
        'method': 'AES-256-CBC'
    })


@app.route('/api/security/sign', methods=['POST'])
def sign_data():
    """Sign data using ECDSA"""
    data = request.json.get('data', '')
    
    signature = security.sign_data(data)
    
    return jsonify({
        'data': data,
        'signature': signature,
        'method': 'ECDSA-SECP256k1'
    })


@app.route('/api/security/verify', methods=['POST'])
def verify_signature():
    """Verify digital signature"""
    data = request.json.get('data', '')
    signature = request.json.get('signature', '')
    
    is_valid = security.verify_signature(data, signature)
    
    return jsonify({
        'data': data,
        'signature': signature,
        'is_valid': is_valid,
        'method': 'ECDSA-SECP256k1'
    })


@app.route('/api/ai/anomaly', methods=['POST'])
def detect_anomaly():
    """Detect anomalies in block data"""
    block_data = request.json
    
    result = ai_module.detect_anomaly(block_data)
    
    return jsonify(result)


@app.route('/api/ai/risk', methods=['POST'])
def predict_risk():
    """Predict transaction risk"""
    transaction_data = request.json
    
    result = ai_module.predict_transaction_risk(transaction_data)
    
    return jsonify(result)


@app.route('/api/ai/analyze', methods=['GET'])
def analyze_blockchain():
    """Analyze blockchain patterns"""
    chain = blockchain.get_chain()
    analysis = ai_module.analyze_blockchain_patterns(chain)
    
    return jsonify(analysis)


@app.route('/api/ai/train', methods=['POST'])
def train_ai():
    """Train AI model with current blockchain data"""
    chain = blockchain.get_chain()
    result = ai_module.train_anomaly_detector(chain)
    
    return jsonify(result)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get comprehensive system statistics"""
    chain = blockchain.get_chain()
    stats = blockchain.get_chain_stats()
    analysis = ai_module.analyze_blockchain_patterns(chain)
    health = ai_module.get_blockchain_health_score(chain, stats['is_valid'])
    
    return jsonify({
        'blockchain': stats,
        'analysis': analysis,
        'health': health
    })


if __name__ == '__main__':
    # Create static folder if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    print("=" * 60)
    print("🚀 Blockchain + AI + Security System Starting...")
    print("=" * 60)
    print("📊 Dashboard: http://localhost:5000")
    print("🔗 Blockchain initialized with Genesis block")
    print("🤖 AI/ML module ready")
    print("🔐 Security features active (RSA, AES, ECDSA, Hashing)")
    print("=" * 60)
    
    # Run without reloader to avoid Windows issues
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
