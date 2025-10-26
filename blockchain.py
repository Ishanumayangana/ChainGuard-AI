import hashlib
import json
import time
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import ecdsa


class SecurityModule:
    """Advanced security module with encryption, signing, and hashing"""
    
    def __init__(self):
        # Generate RSA key pair for encryption/decryption
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
        # Generate ECDSA key pair for signing
        self.signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.verifying_key = self.signing_key.get_verifying_key()
    
    def hash_data(self, data, algorithm='sha256'):
        """Hash data using specified algorithm"""
        if algorithm == 'sha256':
            return hashlib.sha256(data.encode()).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(data.encode()).hexdigest()
        elif algorithm == 'md5':
            return hashlib.md5(data.encode()).hexdigest()
        return hashlib.sha256(data.encode()).hexdigest()
    
    def rsa_encrypt(self, message):
        """RSA encryption"""
        try:
            encrypted = self.public_key.encrypt(
                message.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            return f"Encryption error: {str(e)}"
    
    def rsa_decrypt(self, encrypted_message):
        """RSA decryption"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_message)
            decrypted = self.private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted.decode()
        except Exception as e:
            return f"Decryption error: {str(e)}"
    
    def aes_encrypt(self, message, key=None):
        """AES encryption (symmetric)"""
        if key is None:
            key = get_random_bytes(32)  # 256-bit key
        
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
        
        result = {
            'ciphertext': base64.b64encode(ct_bytes).decode(),
            'iv': base64.b64encode(cipher.iv).decode(),
            'key': base64.b64encode(key).decode()
        }
        return result
    
    def aes_decrypt(self, ciphertext, key, iv):
        """AES decryption"""
        try:
            key_bytes = base64.b64decode(key)
            iv_bytes = base64.b64decode(iv)
            ct_bytes = base64.b64decode(ciphertext)
            
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
            return pt.decode()
        except Exception as e:
            return f"Decryption error: {str(e)}"
    
    def sign_data(self, data):
        """Sign data using ECDSA"""
        signature = self.signing_key.sign(data.encode())
        return base64.b64encode(signature).decode()
    
    def verify_signature(self, data, signature):
        """Verify ECDSA signature"""
        try:
            sig_bytes = base64.b64decode(signature)
            self.verifying_key.verify(sig_bytes, data.encode())
            return True
        except:
            return False


class Block:
    """Individual block in the blockchain"""
    
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate block hash using SHA-256"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Proof of Work mining"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.nonce
    
    def to_dict(self):
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    """Blockchain with security features"""
    
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.security = SecurityModule()
        self.pending_transactions = []
        self.mining_reward = 10
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block"""
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_block(self, data):
        """Add a new block to the chain"""
        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_timestamp = time.time()
        
        # Encrypt sensitive data
        encrypted_data = self.security.rsa_encrypt(json.dumps(data))
        
        # Sign the data
        signature = self.security.sign_data(json.dumps(data))
        
        block_data = {
            'encrypted_data': encrypted_data,
            'signature': signature,
            'hash': self.security.hash_data(json.dumps(data))
        }
        
        new_block = Block(new_index, new_timestamp, block_data, previous_block.hash)
        new_block.mine_block(self.difficulty)
        
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self):
        """Validate the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check proof of work
            if not current_block.hash.startswith('0' * self.difficulty):
                return False
        
        return True
    
    def get_chain(self):
        """Get the entire blockchain"""
        return [block.to_dict() for block in self.chain]
    
    def get_chain_stats(self):
        """Get blockchain statistics"""
        return {
            'total_blocks': len(self.chain),
            'difficulty': self.difficulty,
            'is_valid': self.is_chain_valid(),
            'latest_block_hash': self.get_latest_block().hash
        }
